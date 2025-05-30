import numpy as np
from scipy.optimize import minimize


def harmonic(x, k, r0) -> float:
    """
    Harmonic potential
    Kb: kcal/mole/A**2
    :param x:
    :param k:
    :param r0:
    :return:
    """
    return 0.5 * k * (x - r0) ** 2


def morse(x, De, a, r0) -> float:
    """
    Morse potential
    :param x:
    :param De:
    :param a:
    :param r0:
    :return:
    """
    return De * (1 - np.exp(-a * (x - r0))) ** 2


def harmonic_angle(x, k, theta0) -> float:
    """
    Harmonic angle potential
    !Ktheta: kcal/mole/rad**2
    :param x:
    :param k:
    :param theta0:
    :return:
    """
    return 0.5 * k * (x - theta0) ** 2


def waterlike_energy_interal(kb, ka, r0, a0, a, r1, r2):
    """
    Calculate the energy of a molecule with 2 bonds and 1 angle
    :param kb:
    :param ka:
    :param r0:
    :param a0:
    :param a:
    :param r1:
    :param r2:
    :return:
    """
    E = 0
    E += harmonic(r1, kb, r0)
    E += harmonic(r2, kb, r0)
    E += harmonic_angle(a, ka, a0)
    return E


def dcmlike_energy_interal(CCL_k, CCL_r0, CH_k, CH_r0, ClCCl_k,
                           ClCCl_a0, ClCH_k, ClCH_a0, HCH_k, HCH_a0,
                           r1, r2, r3, r4, a1, a2, a3, a4, a5, a6
                           ):
    """
    """
    E = 0
    E += harmonic(r1, CCL_k, CCL_r0)
    E += harmonic(r2, CCL_k, CCL_r0)
    E += harmonic(r3, CH_k, CH_r0)
    E += harmonic(r4, CH_k, CH_r0)

    E += harmonic_angle(a1, ClCCl_k, ClCCl_a0)
    E += harmonic_angle(a2, ClCH_k, ClCH_a0)
    E += harmonic_angle(a3, ClCH_k, ClCH_a0)
    E += harmonic_angle(a4, ClCH_k, ClCH_a0)
    E += harmonic_angle(a5, ClCH_k, ClCH_a0)
    E += harmonic_angle(a6, HCH_k, HCH_a0)

    return E


H2KCALMOL = 627.503


class FitBonded:
    """
    Takes a DF with monomer energies and internal DoFs,
    and fits the parameters of the internal DoFs
    """

    def __init__(self, df, min_m_E):
        self.df = df.copy()
        #  make sure the keys are the correct type
        self.df["m_ENERGY"] = self.df["m_ENERGY"].astype(np.float64)
        # print(self.df.keys())

        self.min_m_E = min_m_E

        sum_monomer_df = self.df.groupby(
            "key", group_keys=True
        ).sum()  # .apply(lambda x: x)

        # print(sum_monomer_df.keys())

        self.sum_monomer_df = sum_monomer_df

        print("Fitting parameters: kb, ka, r0, a0")
        self.x0 = np.array([1, 1, 1, 2])

        self.res = minimize(self.get_loss, self.x0, tol=1e-6)

        self.x = self.res.x

        self.kb, self.ka, self.r0, self.a0 = self.x

        self.sum_monomer_df = (
            self.get_loss_df(self.x).groupby("key", group_keys=True).sum()
        )  # .apply(lambda x: x)

        self.sum_monomer_df["m_ENERGY"] = (
            self.sum_monomer_df["m_ENERGY"].astype(np.float64).interpolate()
        )

        self.sum_monomer_df["m_E_tot"] = (
                self.sum_monomer_df["m_ENERGY"] - self.min_m_E * H2KCALMOL * 20
        )

        self.sum_monomer_df["p_m_E_tot"] = (
                self.sum_monomer_df["E_pred"] + self.min_m_E * H2KCALMOL * 20
        )

    def get_loss_df(self, x):
        """Return the loss function applied to a dataframe"""
        df = self.df.copy()
        E_pred = []
        for a, r1, r2 in zip(df["a"], df["r1"], df["r2"]):
            a = np.deg2rad(a)
            E_pred.append(waterlike_energy_interal(*x, a, r1, r2))
        df["E_pred"] = E_pred
        df["m_ENERGY"] = df["m_ENERGY"] * H2KCALMOL
        df["m_ENERGY"] = df["m_ENERGY"] - self.min_m_E * H2KCALMOL
        df["SE"] = (df["E_pred"] - df["m_ENERGY"]) ** 2
        return df

    def get_loss(self, x):
        """Return the loss function"""
        df = self.get_loss_df(x)
        MSE = df["SE"].mean()
        return MSE


class FitBondedDCM:
    """
    Takes a DF with monomer energies and internal DoFs,
    and fits the parameters of the internal DoFs
    """

    def __init__(self, df, min_m_E):
        self.df = df.copy()
        #  make sure the keys are the correct type
        self.df["m_ENERGY"] = self.df["m_ENERGY"].astype(np.float64)
        # print(self.df.keys())

        self.min_m_E = min_m_E

        sum_monomer_df = self.df.groupby(
            "key", group_keys=True
        ).sum()  # .apply(lambda x: x)

        # print(sum_monomer_df.keys())

        self.sum_monomer_df = sum_monomer_df

        print(
            "Fitting parameters: CCL_k, CCL_r0, CH_k, CH_r0, ClCCl_k, "
            "ClCCl_a0", "ClCH_k", "ClCH_a0", "HCH_k", "HCH_a0"
        )
        self.x0 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        self.res = minimize(self.get_loss, self.x0, tol=1e-6)

        self.x = self.res.x

        self.kb, self.ka, self.r0, self.a0 = self.x

        self.sum_monomer_df = (
            self.get_loss_df(self.x).groupby("key", group_keys=True).sum()
        )  # .apply(lambda x: x)

        self.sum_monomer_df["m_ENERGY"] = (
            self.sum_monomer_df["m_ENERGY"].astype(np.float64).interpolate()
        )

        self.sum_monomer_df["m_E_tot"] = (
                self.sum_monomer_df["m_ENERGY"] - self.min_m_E * H2KCALMOL * 20
        )

        self.sum_monomer_df["p_m_E_tot"] = (
                self.sum_monomer_df["E_pred"] + self.min_m_E * H2KCALMOL * 20
        )

    def get_loss_df(self, x):
        """Return the loss function applied to a dataframe"""
        df = self.df.copy()
        E_pred = []
        for a, r1, r2 in zip(df["a"], df["r1"], df["r2"]):
            a = np.deg2rad(a)
            E_pred.append(waterlike_energy_interal(*x, a, r1, r2))
        df["E_pred"] = E_pred
        df["m_ENERGY"] = df["m_ENERGY"] * H2KCALMOL
        df["m_ENERGY"] = df["m_ENERGY"] - self.min_m_E * H2KCALMOL
        df["SE"] = (df["E_pred"] - df["m_ENERGY"]) ** 2
        return df

    def get_loss(self, x):
        """Return the loss function"""
        df = self.get_loss_df(x)
        MSE = df["SE"].mean()
        return MSE
