# Monte Carlo Neutron Transport — Stage II

Stage I showed that random sampling could converge onto π. This project 
takes the same framework and applies it to something physical. Neutron 
transport through a material slab, and whether the mathematics behind 
it actually holds up when you simulate it from scratch.

## What this is

A Monte Carlo simulation of neutrons traveling through a material slab. 
Each neutron gets a random free path length sampled from the exponential 
distribution, and the question is simple: does it make it through or 
does it get absorbed? By running that a few hundred thousand times and a 
transmission fraction emerges.

The interesting part is that this fraction converges to e^(-Σx), the 
Beer-Lambert attenuation law, without ever assuming that's what the 
answer should be. It falls out of the random sampling itself, which is
why it isn't just a numerical exercise.

## What I found

- The simulation recovers the Beer-Lambert law across all tested 
  thicknesses and materials, agreeing with the analytical prediction 
  to within statistical uncertainty every time
- The 1/√N convergence from Stage I reappears here exactly, which 
  confirmed for me that this is a property of Monte Carlo methods 
  in general, not something specific to estimating π
- The difference between materials is striking. Light water stops 
  neutrons within a couple of centimetres. Heavy water barely 
  attenuates them over 10 cm. That gap of roughly 17x in mean free 
  path is exactly why different reactor designs use different 
  moderators

## The math behind it

The free path length follows an exponential distribution because 
nuclear collisions are memoryless. The probability of a collision 
in the next tiny slice of material is always the same, regardless 
of how far the neutron has already traveled. That one physical 
fact leads directly to an ODE, which solves to give e^(-Σx). The 
simulation is essentially a numerical proof of that derivation.

## Files

- `neutron_transport.py` — full simulation code
- `transmission_vs_thickness.png` — MC vs analytical result
- `convergence.png` — 1/√N error scaling
- `material_comparison.png` — light water, iron, graphite, heavy water
- `Monte_Carlo_Simulation_of_Neutron_Transport.pdf` — full research paper

## Part of a larger project

- **Stage I** — Monte Carlo estimation of π
- **Stage II** (this repo) — Neutron transport, Beer-Lambert law 
  verified from first principles
- **Stage III** — Full reactor criticality simulation using OpenMC 
  (in progress)
