import json
from matplotlib import pyplot as plt

with open ('041272f1-1d6a-5f6d-b0e0-199c13a1d725.json') as f:
    workflow_result = json.load(f)

coupled_cluster_energy = -1.136189454101414

for task in workflow_result.values():
    if task['class'] == 'optimize-variational-circuit':
        value_history = list(map(lambda t: t['value']['value'],
                            task['optimization-results']['history']))
    if task['class'] == 'run-psi4':
        if task['inputParam:method'].lower() == 'scf':
            hartree_fock_energy = task['energycalc-results']['energy']
        elif task['inputParam:method'].lower() == 'ccsd(t)':
            coupled_cluster_energy = task['energycalc-results']['energy']

plt.figure()
plt.plot(value_history, marker='o', linestyle='None', label='VQE')
plt.axhline(y=hartree_fock_energy, label='Hartree-Fock', color='k')
plt.axhline(y=coupled_cluster_energy, label='CCSD(T)', color='g')
plt.xlabel('Function evaluation')
plt.ylabel('Energy (Ha)')
plt.legend()
plt.tight_layout()
plt.show()
