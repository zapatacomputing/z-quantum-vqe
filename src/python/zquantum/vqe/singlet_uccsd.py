from zquantum.core.interfaces.ansatz import Ansatz
from zquantum.core.interfaces.ansatz_utils import (
    ansatz_property,
    invalidates_parametrized_circuit,
)
from zquantum.core.circuit import Circuit
from openfermion.utils import uccsd_singlet_paramsize, uccsd_singlet_generator
from overrides import overrides
from .utils import exponentiate_fermion_operator
from typing import List, Optional
import numpy as np


class SingletUCCSDAnsatz(Ansatz):

    supports_parametrized_circuits = False
    transformation = ansatz_property("transformation")

    def __init__(
        self,
        number_of_layers: int,
        number_of_spatial_orbitals: int,
        number_of_alpha_electrons: int,
        transformation: str = "Jordan-Wigner",
    ):
        """ 
        Ansatz class representing Singlet UCCSD Ansatz.

        Args:
            number_of_layers: number of layers of the ansatz.
            number_of_spatial_orbitals: number of spatial orbitals.
            number_of_alpha_electrons: number of alpha electrons.
            transformation: transformation used for translation between fermions and qubits.

        Attributes:
            number_of_beta_electrons: number of beta electrons (equal to number_of_alpha_electrons).
            number_of_electrons: total number of electrons (number_of_alpha_electrons + number_of_beta_electrons).
            number_of_qubits: number of qubits required for the ansatz circuit.
            number_of_params: number of the parameters that need to be set for the ansatz circuit.
        """
        super().__init__(number_of_layers)
        self._number_of_spatial_orbitals = number_of_spatial_orbitals
        self._number_of_alpha_electrons = number_of_alpha_electrons
        self._transformation = transformation
        self._assert_number_of_spatial_orbitals()

    @property
    def number_of_spatial_orbitals(self):
        return self._number_of_spatial_orbitals

    @invalidates_parametrized_circuit
    @number_of_spatial_orbitals.setter
    def number_of_spatial_orbitals(self, new_number_of_spatial_orbitals):
        self._number_of_spatial_orbitals = new_number_of_spatial_orbitals
        self._assert_number_of_spatial_orbitals()

    @property
    def number_of_qubits(self):
        return self._number_of_spatial_orbitals * 2

    @property
    def number_of_alpha_electrons(self):
        return self._number_of_alpha_electrons

    @invalidates_parametrized_circuit
    @number_of_alpha_electrons.setter
    def number_of_alpha_electrons(self, new_number_of_alpha_electrons):
        self._number_of_alpha_electrons = new_number_of_alpha_electrons
        self._assert_number_of_spatial_orbitals()

    @property
    def _number_of_beta_electrons(self):
        return self._number_of_alpha_electrons

    @property
    def number_of_electrons(self):
        return self._number_of_alpha_electrons + self._number_of_beta_electrons

    @property
    def number_of_params(self) -> int:
        """
        Returns number of parameters in the ansatz.
        """
        return uccsd_singlet_paramsize(
            n_qubits=self.number_of_qubits, n_electrons=self.number_of_electrons,
        )

    @overrides
    def _generate_circuit(self, params: Optional[np.ndarray] = None) -> Circuit:
        """
        Returns a parametrizable circuit represention of the ansatz.
        Args:
            params: parameters of the circuit. 
        """
        circuit = Circuit()
        circuit.gates = []

        # Prepare initial state
        for i in range(n_electrons):
            qubit_index = n_electrons - i - 1
            circuit.gates.append(Gate("X", Qubit(qubit_index)))

        # Build UCCSD generator
        fermion_generator = uccsd_singlet_generator(
            params,
            self.number_of_qubits,
            self.number_of_electrons,
            anti_hermitian=True,
        )

        evolution_operator = exponentiate_fermion_operator(
            fermion_generator, self._transformation
        )

        circuit += Circuit(evolution_operator)
        return circuit

    def _assert_number_of_spatial_orbitals(self):
        if self._number_of_spatial_orbitals < 2:
            raise (
                ValueError(
                    "Number of spatials orbitals must be greater or equal 2 and is {0}.".format(
                        self._number_of_spatial_orbitals
                    )
                )
            )
        if self._number_of_spatial_orbitals <= self._number_of_alpha_electrons:
            raise (
                ValueError(
                    "Number of spatial orbitals must be greater than number_of_alpha_electrons and is {0}".format(
                        self._number_of_spatial_orbitals
                    )
                )
            )
