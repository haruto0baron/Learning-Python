import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "Noto Sans CJK JP"
import os


# =============================
# 設定
# =============================

SIZE = 100          # 世界の大きさ
MAX_STEPS = 500     # 最大世代
TRIALS = 20         # 各密度の試行回数

densities = np.arange(
    0.05,
    1.00,
    0.05
)


# 保存フォルダ
os.makedirs(
    "lifegame_results",
    exist_ok=True
)


# =============================
# ライフゲーム処理
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


    alive = (
        (world == 1)
        &
        ((neighbors == 2) | (neighbors == 3))
    )


    born = (
        (world == 0)
        &
        (neighbors == 3)
    )


    new_world = np.zeros_like(world)

    new_world[alive | born] = 1


    return new_world



# =============================
# 初期世界作成
# =============================

def create_world(density):

    return (
        np.random.random((SIZE, SIZE))
        <
        density
    ).astype(int)



# =============================
# 1回シミュレーション
# =============================

def simulate(density):

    world = create_world(density)

    history = []


    for step in range(MAX_STEPS):

        alive_cells = np.sum(world)

        history.append(alive_cells)


        new_world = next_generation(world)


        # 変化なし
        if np.array_equal(
            world,
            new_world
        ):
            break


        world = new_world



    final_cells = np.sum(world)


    extinct = (
        final_cells == 0
    )


    return (
        step,
        final_cells,
        extinct,
        history
    )



# =============================
# 実験開始
# =============================

results = []


print("実験開始")


for density in densities:

    times = []
    populations = []
    extinct_count = 0


    for i in range(TRIALS):

        steps, final, extinct, history = simulate(
            density
        )


        times.append(steps)

        populations.append(final)


        if extinct:
            extinct_count += 1



    results.append(
        [
            density,
            np.mean(times),
            np.mean(populations),
            extinct_count / TRIALS * 100
        ]
    )


    print(
        f"密度 {density:.2f} 完了"
    )



# =============================
# 表作成
# =============================

df = pd.DataFrame(
    results,
    columns=[
        "初期密度",
        "平均安定世代",
        "平均最終生存セル数",
        "全滅率(%)"
    ]
)


df = df.round(2)


print("\n===== 実験結果 =====")

print(df)



# CSV保存

df.to_csv(
    "lifegame_results/result.csv",
    index=False,
    encoding="utf-8-sig"
)



# =============================
# グラフ1
# 安定までの時間
# =============================

plt.figure(
    figsize=(8,5)
)


plt.plot(
    df["初期密度"],
    df["平均安定世代"],
    marker="o"
)


plt.xlabel(
    "初期密度"
)

plt.ylabel(
    "平均安定世代"
)


plt.title(
    "初期密度と安定までの時間"
)


plt.grid()


plt.savefig(
    "lifegame_results/time.png",
    dpi=300
)


plt.show()



# =============================
# グラフ2
# 最終生存数
# =============================

plt.figure(
    figsize=(8,5)
)


plt.plot(
    df["初期密度"],
    df["平均最終生存セル数"],
    color="green",
    marker="o"
)


plt.xlabel(
    "初期密度"
)


plt.ylabel(
    "最終生存セル数"
)


plt.title(
    "初期密度と最終生存セル数"
)


plt.grid()


plt.savefig(
    "lifegame_results/population.png",
    dpi=300
)


plt.show()



# =============================
# グラフ3
# 全滅率
# =============================

plt.figure(
    figsize=(8,5)
)


plt.bar(
    df["初期密度"],
    df["全滅率(%)"],
    width=0.04
)


plt.xlabel(
    "初期密度"
)


plt.ylabel(
    "全滅率(%)"
)


plt.title(
    "初期密度と全滅率"
)


plt.grid(
    axis="y"
)


plt.savefig(
    "lifegame_results/extinction.png",
    dpi=300
)


plt.show()



print("\n完了しました")
print("lifegame_results フォルダを確認してください")
