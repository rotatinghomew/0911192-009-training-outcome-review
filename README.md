# 转班与分母变化下的培训成效拨款

培训转承、核验与拨付的分期记录；均为合成学员。
这里的记录全部为合成资料。日期按当地日历解释，未附时区的时间使用东八区。

## 交接资料

CSV 使用 UTF-8 和逗号分隔。值留空表示这条资料未给出该字段，不等于零。
`data/schema.json` 登记表头与跨表编号关系；`data/policy.json` 保存本期业务配置。

- `data/learners.csv`：stratum 是入学时状态，不因事后就业改变；eligible 来自项目资格名册。 字段：`learner`, `stratum`, `eligible`。
- `data/courses.csv`：实践 part 为 lab，通识为 intro；空完成日期不认结业。 字段：`course`, `learner`, `school`, `part`, `accepted`, `completed`。
- `data/handoffs.csv`：跨校有效确认按实际生效日核对责任；撤回明确指原方向。 字段：`receipt`, `learner`, `from_school`, `to_school`, `effective`, `received`, `state`。
- `data/verification.csv`：未查到 contact_lost 和核对未就业 unemployed 分开；空持续日为不可验证。 字段：`evidence`, `learner`, `assessed`, `received`, `result`, `days`。
- `data/seat_actions.csv`：hold 保留，issued 已通知，manual 人工裁定；相同通知号可追加冲抵，以负数表示。 字段：`notice`, `school`, `period`, `seats`, `state`, `posted`。

## 资料校验

使用 Python 3.11.2 标准库，不需要安装扩展包。资料入口只核查交接格式，不计算业务结果。

```sh
python3 inspect_inputs.py
python3 -m unittest -v
```
