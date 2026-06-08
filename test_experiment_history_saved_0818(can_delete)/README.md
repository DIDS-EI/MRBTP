# Experiment Archive (2025-08-18 snapshot)

> 标记 `(can_delete)` 仅说明本目录不被任何活跃代码引用、可安全归档；
> 其内容仍是对论文实验的**完整历史快照**，整理目的是让"代码 ↔ 输出图片/数据"
> 一一配对，便于复现与回溯。
>
> **2026-06-08 第二轮**：把仓库根目录下的 6 个"裸输出"目录（`test_composite_action/`、
> `test_subgoal/`、`test_gridworld/`、`test_exp1_snapshots/`、`test_exp2_vh_snapshots/`、
> `test_exp_numsim_snapshots/`）全部并入本 archive 中的同名实验目录。
>
> **2026-06-08 第三轮（本次）**：
> 1. 把 `other_files/test_composite_action/` 的 4 张 SVG 并入 archive `legacy_composite_action/outputs/`（重名加 `_otherfiles` 后缀）。
> 2. 把 archive 中所有子目录从 `test_aaa_*` / `test_*` 重命名为 `legacy_*`，让"已归档历史版本"一目了然，与仓库当前活跃的 `test_experiment/` 做出区分。
> 3. 整理 `test_multi_minigrid_single_demo/`（仓库根目录 demo 入口）：脚本与示例输出分离。

## 目录约定

每个 `legacy_*/` 子目录统一采用如下子结构（按需出现）：

| 子目录                | 用途                                             |
| --------------------- | ------------------------------------------------ |
| `code/`               | 生成 / 评测脚本（`*.py`）                         |
| `outputs/`            | 运行产物：`*.bt` / `*.svg` / `*.png` / `*.pdf` / `*.csv` |
| `data/`               | 中间数据：`*.csv` / `*.json` / `*.pkl` / `*.txt`  |
| `scenario_*/`         | 特定场景（任务变体）的独立快照                    |
| `*_snapshots/`        | 同一实验不同时间/不同设置的产物分组               |

> 当 `outputs/` 中存在重名文件且内容不同（例如来自仓库根目录的 live 版本 vs 旧 archive），
> 新并入的版本统一带后缀（`_live.svg` / `_otherfiles.svg`）以避免覆盖。

## 命名对照（旧 → 新）

```
test_aaa_exp1            → legacy_exp1_robustness_parallelism
test_aaa_vh_exp2         → legacy_exp2_vh_subtree_llms
test_composite_action    → legacy_composite_action
test_exp_numsim          → legacy_numsim
test_fruit_env           → legacy_fruit_env_demo
test_gridworld           → legacy_gridworld
test_subgoal             → legacy_subgoal
test_virtualhome         → legacy_virtualhome
```

## 各实验目录索引

### 1. `legacy_exp1_robustness_parallelism/` — MiniGrid 并行性 / 鲁棒性主实验
- `code/`：`key_room_ball*.py`、`*_并行性实验_*.py`、`*_鲁棒性实验_*.py`、`*_parallelism.py`、`*_robustness.py`
- `outputs/`：`agent-{0..3}.svg`（运行可视化）+ `robot-{0..9}.bt`
- `plots_robustness_parallelism/`：3 个绘图脚本 + 4 个论文 PDF
- `scenario_door_always_open/`：「门一直保持 open」消融实验快照
- **对应当前活跃实验**：`test_experiment/exp1_robustness_parallelism/`

### 2. `legacy_exp2_vh_subtree_llms/` — VirtualHome × LLM 大规模实验
- `code/`：`01_llm_get_subtree*.py`、`02_load_json_evaluate*.py`、`03_test.py`、`check_two_datas.py`、`test_generate_json.py`
- `outputs/`：~40 张产物 — `agent-0..3.svg`、`robot-{0..3}.{bt,svg,png}`、`robot-*_live.svg`、`data{0..3}-walkto*.svg`
- `data/`：~80 个 csv/json/txt 数据切片
- `llm_data/` / `llm_outputs_0813/` / `llm_results_0816/`：三个时间点 LLM 输入输出
- `scenario_materials/`：21 张论文素材 SVG
- `tree_svg_snapshots/`：38 张 BT 渲染快照
- **对应当前活跃实验**：`test_experiment/exp2_subtree_llms/`

### 3. `legacy_composite_action/` — 组合动作 (PreAdd/Del) 实验
- `code/`：`composite_action.py`、`example_test_3.py`、`test.py`、`test_7room.py`、`测试组合动作的 pre add del.py`
- `outputs/`：22 个产物 — `robot-0..2.{bt,svg}`、`agent-0..2.svg` (含 `_otherfiles` 后缀的 2 个外部副本)、`data*-{getkeyandopendoor,move*betweenrooms}.svg`
- `scenario_two_agents_door_key/`：双智能体「开门 + 拿钥匙」场景：2 .bt + 4 .svg + `subtree/` 子树渲染
- `scenario_task_demo_0716/`：2025/07/16 任务展示 demo（2 SVG）

### 4. `legacy_numsim/` — 数值模拟 / 复杂度统计实验
- `code/`：`01_main_generate_data*.py`、`data_generate*.py`、`mabtp_test.py`、`maobtp_test.py`、`num_cabtp.py`、`simulation.py`、`03 generate_and_test.py`
- `outputs/`：`datacmp_a{1,2,4}_d0.svg`、`robot-{0,1}.{bt,svg}`、`robot-{0,1}_live.svg`、`detailed_results_*.csv`、`summary_results_*.csv`
- `data/valid_data_depth2_branch3_agent2/`：16 个 `*.pkl` 数据文件
- `unit_tests/`：单元测试脚本
- `other_files_saved/`：早期版本备份 + 失败用例 `intra_extra_tree_no_result/`

### 5. `legacy_fruit_env_demo/` — Fruit 环境 demo
- `code/`：`action_list.py`、`random_actions.py`（纯 demo，无图片产物）

### 6. `legacy_gridworld/` — 早期 MiniGrid 接入实验
- `code/`：`ma-bt-run.py`、`mabt_*.py`、`mabtp_minigrid_test.py`、`custom_env.py`
- `outputs/`：`agent-{0,1}.svg`、`agent-{0,1}_live.svg`、`robot-{0..2}.bt`、`*.btml`

### 7. `legacy_subgoal/` — 子目标分配 / 集中式规划
- `code/`：`bt_run_subgoal.py`、`centralized planning.py`
- `outputs/`：`centralize.bt`、`subgoal{,1}.bt` + 5 张运行可视化 + `backup/`（4 份 BT 历史）

### 8. `legacy_virtualhome/` — VirtualHome 直接接入测试
- `code/`：`camera.py`、`multi_character.py`、`test_run_dmr.py`
- `outputs/`：`script/`、`script - 副本/`（VirtualHome 引擎日志）

### 附：`MiniGird所有场景.txt`
（原文件名手误，保留以避免破坏外链）—— MiniGrid 场景总清单参考。

## 整理操作摘要

### 第一轮（首次归档）
1. 删除 `test_exp_numsim/小例子存档/`（3 SVG 与父目录完全相同）。
2. 改名 6 个中文/不规范命名子目录为英文语义命名。
3. 各实验目录顶层散落文件统一收纳到 `code/` + `outputs/` (+ `data/`)。

### 第二轮（2026-06-08）
1. 合并 `test_composite_action/`（live ↔ archive）：17 SVG → `outputs/`，2 个子目录改名 `scenario_*`。
2. 合并 `test_subgoal/`、`test_gridworld/`、`test_exp1_snapshots/`、`test_exp2_vh_snapshots/`、`test_exp_numsim_snapshots/`。
3. 重名冲突统一加 `_live` 后缀。

### 第三轮（2026-06-08，本次）
1. 合并 `other_files/test_composite_action/`（4 SVG）→ `legacy_composite_action/outputs/`（重名加 `_otherfiles`）。
2. archive 子目录全量重命名 `test_*` → `legacy_*`，与活跃的 `test_experiment/` 区分。
3. 整理 `test_multi_minigrid_single_demo/`：脚本（`main.py` / `main2.py`）保留顶层，示例输出（4 BT + 8 SVG）移入 `example_outputs/`。

## 仓库根目录效果（最终）
合并后仓库根目录的 `test_*` 只剩：
- `test_cfg/` — 配置脚本（被 `test_experiment/` 引用）
- `test_experiment/` — 论文当前实验入口（exp1 / exp2 / exp3）
- `test_multi_minigrid_single_demo/` — README 引用的 demo 入口（含 `example_outputs/`）

其余历史输出全部归集到本 archive，子目录统一 `legacy_*` 前缀。
