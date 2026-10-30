# K3 Surface Mirror Symmetry

## Package List

(find these in the `src` folder)

- **k3_example**: the code related to the studied polynomial `x^3y + y^3x + z^3w + w^3z`.
  - the `output` lists the intersection matrix for X1, X2, and X4 along with the curves
  - the `x1`, `x2`, and `x4` folders contain code related to each specific surface. In each case, you can run `ranks.py` to compute the rank of various sublattices
- **k3_polynomial_generator**: code to generate all possible polynomials based upon the 95 known possible weights
  - run `generate.py` to see the full list of polynomials
  - in the `output`, there is a json list of all the exponent matrices corresponding to the possible polynomials, each together with the weight used to generate the polynomial 

## Usage

This package uses uv for Python version and dependency management. First install uv. Then, in this directory run `uv sync`, which will automatically install dependencies. After that, you can run files with `uv run path/to/file.py`.