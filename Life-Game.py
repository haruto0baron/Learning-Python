import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# =============================
# Settings
# =============================

SIZE = 100
MAX_STEPS = 500
TRIALS = 20

densities = np.arange(
    0.05,
    1.00,
    0.05
)


os.makedirs(
    "lifegame_results",
    exist_ok=True
)


# =============================
# Game of Life Rule
# =============================

def next_generation(world):

    neighbors = (
        np.roll(world, 1, 0) +
        np.roll(world, -1, 0) +
        np.roll(world, 1, 1) +
        np.roll(world, -1, 1) +
        np.roll(np.roll(world, 1, 0), 1, 1) +
        np.roll(np.roll(world, 1, 0), -1, 1) +
        np.roll(np.roll(world, -1, 0), 1, 1) +
        np.roll(np.roll(world, -1, 0), -1, 1)
    )


    survive = (
        (world == 1)
        &
        ((neighbors == 2) | (neighbors == 3))
    )


    birth = (
        (world == 0)
        &
        (neighbors == 3)
    )


    new_world = np.zeros_like(world)

    new_world[survive | birth] = 1

    return new_world



# =============================
# Create Initial World
# =============================

def create_world(density):

    return (
        np.random.random((SIZE, SIZE))
        < density
    ).astype(int)



# =============================
# Simulation
# =============================

def simulate(density):

    world = create_world(density)

    history = []


    for step in range(MAX_STEPS):

        alive = np.sum(world)

        history.append(alive)


        new_world = next_generation(world)


        if np.array_equal(
            world,
            new_world
        ):
            break


        world = new_world



    final_population = np.sum(world)

    extinct = (
        final_population == 0
    )


    return (
        step,
        final_population,
        extinct,
        history
    )



# =============================
# Experiment
# =============================

results = []


print("Experiment started")


for density in densities:

    stabilization_times = []
    final_populations = []

    extinct_count = 0


    for i in range(TRIALS):

        steps, final, extinct, history = simulate(
            density
        )


        stabilization_times.append(
            steps
        )

        final_populations.append(
            final
        )


        if extinct:
            extinct_count += 1



    results.append(
        [
            density,
            np.mean(stabilization_times),
            np.mean(final_populations),
            extinct_count / TRIALS * 100
        ]
    )


    print(
        f"Density {density:.2f} completed"
    )



# =============================
# Create Result Table
# =============================

df = pd.DataFrame(
    results,
    columns=[
        "Initial Density",
        "Average Stabilization Generation",
        "Average Final Alive Cells",
        "Extinction Rate (%)"
    ]
)


df = df.round(2)


print("\n===== Results =====")

print(df)



df.to_csv(
    "lifegame_results/result.csv",
    index=False
)



# =============================
# Graph 1
# Stabilization Time
# =============================

plt.figure(figsize=(8,5))

plt.plot(
    df["Initial Density"],
    df["Average Stabilization Generation"],
    marker="o",
    linewidth=2
)


plt.xlabel(
    "Initial Density"
)

plt.ylabel(
    "Average Stabilization Generation"
)


plt.title(
    "Initial Density vs Stabilization Time"
)


plt.grid()


plt.savefig(
    "lifegame_results/stabilization_time.png",
    dpi=300
)


plt.show()



# =============================
# Graph 2
# Final Population
# =============================

plt.figure(figsize=(8,5))


plt.plot(
    df["Initial Density"],
    df["Average Final Alive Cells"],
    marker="o",
    color="green",
    linewidth=2
)


plt.xlabel(
    "Initial Density"
)


plt.ylabel(
    "Average Final Alive Cells"
)


plt.title(
    "Initial Density vs Final Population"
)


plt.grid()


plt.savefig(
    "lifegame_results/final_population.png",
    dpi=300
)


plt.show()



# =============================
# Graph 3
# Extinction Rate
# =============================

plt.figure(figsize=(8,5))


plt.bar(
    df["Initial Density"],
    df["Extinction Rate (%)"],
    width=0.04
)


plt.xlabel(
    "Initial Density"
)


plt.ylabel(
    "Extinction Rate (%)"
)


plt.title(
    "Initial Density vs Extinction Rate"
)


plt.grid(
    axis="y"
)


plt.savefig(
    "lifegame_results/extinction_rate.png",
    dpi=300
)


plt.show()



print("\nFinished!")
print("Check the lifegame_results folder.")