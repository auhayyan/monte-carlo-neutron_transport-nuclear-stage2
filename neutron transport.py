import numpy as np
import matplotlib.pyplot as plt
import time
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ── Core simulation ────────────────────────────────────────────────────────────

def simulate_transmission(N, thickness, sigma):
    """
    Simulate N neutrons traveling through a slab of given thickness.
    Each neutron's free path is sampled from the exponential distribution
    using inverse transform sampling: d = -ln(r) / sigma.
    Returns the MC transmission fraction, analytical value, uncertainty, and error.
    """

    # Sample one free path per neutron
    r = np.random.default_rng().random(N)
    free_paths = -np.log(r) / sigma

    # A neutron transmits if its free path exceeds the slab thickness
    n_transmitted = np.sum(free_paths > thickness)
    T_mc = n_transmitted / N

    T_analytical = np.exp(-sigma * thickness)

    # Uncertainty from Bernoulli variance: sqrt(p(1-p)/N)
    sigma_T = np.sqrt(T_mc * (1 - T_mc) / N)
    error = abs(T_mc - T_analytical)

    return T_mc, T_analytical, sigma_T, error


# ── Experiment 1: transmission vs thickness ────────────────────────────────────

def experiment_thickness_sweep():
    sigma = 1.0
    N = 500_000

    # Sweep from 0 to 5 mean free paths (5/sigma cm)
    thicknesses = np.linspace(0, 5 / sigma, 60)

    T_mc_values = []
    T_analytical_values = []
    uncertainty_values = []

    for x in thicknesses:
        T_mc, T_analytical, sigma_T, _ = simulate_transmission(N, x, sigma)
        T_mc_values.append(T_mc)
        T_analytical_values.append(T_analytical)
        uncertainty_values.append(sigma_T)

    T_mc_values = np.array(T_mc_values)
    T_analytical_values = np.array(T_analytical_values)
    uncertainty_values = np.array(uncertainty_values)

    plt.figure(figsize=(8, 5))
    plt.plot(thicknesses, T_analytical_values,
             color='steelblue', linewidth=2,
             label=r'Analytical: $e^{-\Sigma x}$')
    plt.errorbar(thicknesses, T_mc_values,
                 yerr=2 * uncertainty_values,
                 fmt='o', markersize=3, color='coral',
                 alpha=0.6, label='Monte Carlo (±2σ)')

    plt.xlabel(r'Thickness $x$ (cm)')
    plt.ylabel('Transmission fraction P(x)')
    plt.title(r'Neutron Transmission vs Slab Thickness ($\Sigma = 1.0$ cm$^{-1}$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('transmission_vs_thickness.png', dpi=150)
    plt.show()

    print("Experiment 1 complete.")


# ── Experient 2: convergence of MC error with N ───────────────────────────────

def experiment_convergence():
    thickness = 1.0
    sigma = 1.0

    sample_sizes = [100, 500, 1_000, 5_000, 10_000,
                    50_000, 100_000, 500_000, 1_000_000]

    errors = []
    uncertainties = []

    for N in sample_sizes:
        T_mc, T_analytical, sigma_T, error = simulate_transmission(
            N, thickness, sigma
        )
        errors.append(error)
        uncertainties.append(sigma_T)

    sample_sizes = np.array(sample_sizes)
    errors = np.array(errors)

    # Theoretical 1/sqrt(N) curve for reference
    p = np.exp(-sigma * thickness)
    theory = np.sqrt(p * (1 - p) / sample_sizes)

    plt.figure(figsize=(8, 5))
    plt.loglog(sample_sizes, errors,
               'o-', color='coral', label='|MC error|', linewidth=1.5)
    plt.loglog(sample_sizes, theory,
               '--', color='steelblue',
               label=r'Theory: $\sqrt{p(1-p)/N}$', linewidth=2)

    plt.xlabel('Number of neutron histories N')
    plt.ylabel('Absolute error')
    plt.title('Monte Carlo Convergence: Error vs N')
    plt.legend()
    plt.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig('convergence.png', dpi=150)
    plt.show()

    print("Experiment 2 complete.")


# ── Experiment 3: compare attenuation across real reactor materials ────────────

def experiment_materials():

    # Cross-sections for thermal neutrons (cm^ -1)
    materials = {
        'Light water':  3.0,
        'Iron':         1.6,
        'Graphite':     0.38,
        'Heavy water':  0.18,
    }

    thicknesses = np.linspace(0, 10, 80)
    colors = ['steelblue', 'coral', 'seagreen', 'mediumpurple']

    plt.figure(figsize=(9, 5))

    for (material, sigma), color in zip(materials.items(), colors):
        T_analytical = np.exp(-sigma * thicknesses)
        plt.plot(thicknesses, T_analytical,
                 color=color, linewidth=2,
                 label=f'{material} (Σ={sigma} cm⁻¹)')

    plt.xlabel('Thickness x (cm)')
    plt.ylabel('Transmission fraction')
    plt.title('Neutron Transmission: Material Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('material_comparison.png', dpi=150)
    plt.show()

    print("Experiment 3 complete.")


# ── Run everything ─────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Saanity Check
    print("Sanity check (N=100,000, x=1.0cm, Σ=1.0):")
    T_mc, T_analytical, sigma_T, error = simulate_transmission(100_000, 1.0, 1.0)
    print(f"  MC Transmission:         {T_mc:.5f}")
    print(f"  Analytical  (e^-1):      {T_analytical:.5f}")
    print(f"  Uncertainty (± σ_T):     {sigma_T:.5f}")
    print(f"  Error:                   {error:.5f}")
    print()

    print("Running Experiment 1: Transmission vs Thickness...")
    experiment_thickness_sweep()

    print("Running Experiment 2: Convergence...")
    experiment_convergence()

    print("Running Experiment 3: Materials...")
    experiment_materials()

    print("\nAll experiments complete.")