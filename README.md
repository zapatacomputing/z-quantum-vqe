# z-quantum-vqe

[![codecov](https://codecov.io/gh/zapatacomputing/z-quantum-vqe/branch/main/graph/badge.svg?token=XCYDQSBK9V)](https://codecov.io/gh/zapatacomputing/z-quantum-vqe)

## What is it?

`z-quantum-vqe` is a module with basic implementation of Variational Quantum Eigensolver (VQE) to be used with [Orquestra](https://www.orquestra.io) – a platform for performing computations on quantum computers developed by [Zapata Computing](https://www.zapatacomputing.com).

## Usage

### Workflow
In order to use `z-quantum-vqe` in your workflow, you need to add it as an `import` in your Orquestra workflow:

```yaml
imports:
- name: z-quantum-vqe
  type: git
  parameters:
    repository: "git@github.com:zapatacomputing/z-quantum-vqe.git"
    branch: "main"
```

and then add it in the `imports` argument of your `step`:

```yaml
- name: my-step
  config:
    runtime: python3
    imports: [z-quantum-vqe]
```

Once that is done you can:
- use tasks which import `zquantum.vqe` in the python code (see below).

### Python

Here's an example how to do use methods from `z-quantum-vqe` in a Python task:

```python
from zquantum.vqe.ansatz import build_circuit_template
ansatz = build_circuit_template(
              ansatz_type='Singlet UCCSD',
              n_mo=1,
              n_alpha=1,
              n_beta=1,
              transformation='Jordan-Wigner')
```

Even though it's intended to be used with Orquestra, you can also use it as a standalone python module.
In order to install it run `pip install .` from the `src/` directory.


## Development and contribution

You can find the development guidelines in the [`z-quantum-core` repository](https://github.com/zapatacomputing/z-quantum-core).

### Running tests

In order to run tests please run `pytest .` from the main directory.
