"""
财务模型计算器 - 全球一人公司创业全链路指导系统
支持一次性购买和订阅制/SaaS两种商业模型。
用于精确计算收入预测、成本分析、盈亏平衡点和三档场景模拟。
"""
import argparse
import json
import sys
import io
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def calculate_compare_model(traditional_low=30000, traditional_high=50000,
                            ai_low=250, ai_high=1000, currency="USD"):
    """AI vs 传统团队成本对比模型（基于2026年数据）。"""
    trad_mid = (traditional_low + traditional_high) / 2
    ai_mid = (ai_low + ai_high) / 2
    compression_low = 1 - (ai_high / traditional_low)
    compression_high = 1 - (ai_low / traditional_high)

    roles_traditional = [
        "产品经理", "全栈工程师", "UI/UX设计师", "营销专员",
        "客服", "财务/行政"
    ]
    roles_ai_replacement = [
        "AI产品规划(Claude/GPT)", "AI辅助编码(Cursor/Copilot)",
        "AI设计(Midjourney/Figma AI)", "AI营销(Jasper/Copy.ai)",
        "AI客服(自动化)", "AI财务(自动化工具)"
    ]

    return {
        "model_type": "compare",
        "currency": currency,
        "traditional_team": {
            "monthly_cost_low": traditional_low,
            "monthly_cost_high": traditional_high,
            "monthly_cost_mid": round(trad_mid, 2),
            "annual_cost_mid": round(trad_mid * 12, 2),
            "headcount": len(roles_traditional),
            "roles": roles_traditional
        },
        "ai_driven_solo": {
            "monthly_cost_low": ai_low,
            "monthly_cost_high": ai_high,
            "monthly_cost_mid": round(ai_mid, 2),
            "annual_cost_mid": round(ai_mid * 12, 2),
            "headcount": 1,
            "tools": roles_ai_replacement
        },
        "cost_compression": {
            "rate_low": f"{compression_low:.1%}",
            "rate_high": f"{compression_high:.1%}",
            "description": f"AI驱动单人月成本仅为传统团队的{1 - compression_high:.1%}-{1 - compression_low:.1%}，成本压缩{compression_low:.1%}-{compression_high:.1%}"
        },
        "annual_savings": {
            "low": round((traditional_low - ai_high) * 12, 2),
            "high": round((traditional_high - ai_low) * 12, 2),
            "description": f"年节省{round((traditional_low - ai_high) * 12, 2)}-{round((traditional_high - ai_low) * 12, 2)}{currency}"
        },
        "recommendations": [
            "AI工具月成本$250-1000可替代$30000-50000的传统团队，适合一人公司从Day 1启动",
            "初期用AI替代非核心职能（客服/财务/营销），核心产品决策保留人工",
            "随营收增长逐步引入兼职/外包填补AI短板，保持成本结构优势",
            "定期评估AI工具ROI，淘汰低效工具，集中预算到高产工具"
        ]
    }


def calculate_one_time_model(
    fixed_costs, variable_costs, price,
    conservative, moderate, optimistic, currency
):
    """一次性购买模型计算。"""
    if price <= 0:
        return {"error": "单价必须大于0"}
    if price <= variable_costs:
        return {"error": f"单价({price})必须大于单位变动成本({variable_costs})，否则每卖一件都亏损"}

    margin_per_unit = price - variable_costs
    margin_rate = margin_per_unit / price
    breakeven_units = fixed_costs / margin_per_unit
    breakeven_revenue = breakeven_units * price

    scenarios = {}
    for name, units in [("conservative", conservative), ("moderate", moderate), ("optimistic", optimistic)]:
        revenue = price * units
        total_cost = fixed_costs + variable_costs * units
        gross_profit = revenue - total_cost
        net_margin = gross_profit / revenue if revenue > 0 else 0
        scenarios[name] = {
            "monthly": {
                "units": units,
                "revenue": round(revenue, 2),
                "total_cost": round(total_cost, 2),
                "gross_profit": round(gross_profit, 2),
                "net_margin": f"{net_margin:.1%}"
            },
            "annual": {
                "units": units * 12,
                "revenue": round(revenue * 12, 2),
                "total_cost": round(total_cost * 12, 2),
                "gross_profit": round(gross_profit * 12, 2),
                "net_margin": f"{net_margin:.1%}"
            }
        }

    moderate_revenue = price * moderate
    safety_margin = (moderate_revenue - breakeven_revenue) / moderate_revenue if moderate_revenue > 0 else 0

    targets = {}
    for t_name, t_income in [("月入3千", 3000), ("月入1万", 10000), ("月入3万", 30000), ("月入10万", 100000)]:
        req_units = (fixed_costs + t_income) / margin_per_unit
        targets[t_name] = {
            "target_profit": t_income,
            "required_units": round(req_units, 1),
            "required_revenue": round(req_units * price, 2)
        }

    return {
        "model_type": "one_time",
        "currency": currency,
        "inputs": {
            "fixed_costs_monthly": fixed_costs,
            "variable_costs_per_unit": variable_costs,
            "price_per_unit": price,
            "margin_per_unit": round(margin_per_unit, 2),
            "margin_rate": f"{margin_rate:.1%}"
        },
        "breakeven": {
            "units": round(breakeven_units, 1),
            "revenue": round(breakeven_revenue, 2),
            "description": f"每月需卖出{round(breakeven_units, 1)}件，月收入达到{round(breakeven_revenue, 2)}{currency}即可盈亏平衡"
        },
        "scenarios": scenarios,
        "safety_margin": {
            "rate": f"{safety_margin:.1%}",
            "description": _safety_desc(safety_margin)
        },
        "profit_targets": targets,
        "recommendations": _generate_recommendations(margin_rate, safety_margin, breakeven_units, moderate)
    }


def calculate_subscription_model(
    fixed_costs, variable_costs_per_user, monthly_price,
    conservative, moderate, optimistic,
    monthly_churn_rate, currency, cac=0
):
    """订阅制/SaaS模型计算。"""
    if monthly_price <= 0:
        return {"error": "月费必须大于0"}
    if monthly_price <= variable_costs_per_user:
        return {"error": f"月费({monthly_price})必须大于每用户变动成本({variable_costs_per_user})"}

    margin_per_user = monthly_price - variable_costs_per_user
    margin_rate = margin_per_user / monthly_price
    # LTV = margin_per_user / churn_rate
    churn = monthly_churn_rate / 100 if monthly_churn_rate > 1 else monthly_churn_rate
    if churn <= 0:
        churn = 0.05  # 默认5%月流失率
    ltv = margin_per_user / churn
    # 盈亏平衡: fixed_costs / margin_per_user = 需要多少付费用户
    breakeven_users = fixed_costs / margin_per_user

    scenarios = {}
    for name, total_users in [("conservative", conservative), ("moderate", moderate), ("optimistic", optimistic)]:
        monthly_revenue = monthly_price * total_users
        monthly_cost = fixed_costs + variable_costs_per_user * total_users
        monthly_profit = monthly_revenue - monthly_cost
        net_margin = monthly_profit / monthly_revenue if monthly_revenue > 0 else 0
        # 考虑流失: 每月新增用户需弥补流失
        monthly_new_needed = total_users * churn  # 每月需新增用户数维持
        annual_revenue = monthly_revenue * 12
        annual_profit = monthly_profit * 12
        # 首年累计获取量: 维持 steady-state 月增 churn*users 且首年线性累积(简单近似, 见_meta注释)
        # 注：首年累计获取量为近似估算（行业口径），非精确金融指标；以实际运营数据为准
        first_year_acquisitions = round(total_users + total_users * churn * 6)

        scenarios[name] = {
            "monthly": {
                "active_users": total_users,
                "mrr": round(monthly_revenue, 2),
                "total_cost": round(monthly_cost, 2),
                "monthly_profit": round(monthly_profit, 2),
                "net_margin": f"{net_margin:.1%}",
                "new_users_needed": round(monthly_new_needed, 1)
            },
            "annual": {
                "revenue": round(annual_revenue, 2),
                "profit": round(annual_profit, 2),
                "net_margin": f"{net_margin:.1%}",
                "total_acquisitions_needed": first_year_acquisitions
            }
        }

    moderate_mrr = monthly_price * moderate
    breakeven_mrr = breakeven_users * monthly_price
    safety_margin = (moderate_mrr - breakeven_mrr) / moderate_mrr if moderate_mrr > 0 else 0

    targets = {}
    for t_name, t_mrr in [("月入3千", 3000), ("月入1万", 10000), ("月入3万", 30000), ("月入10万", 100000)]:
        req_users = (fixed_costs + t_mrr) / margin_per_user
        targets[t_name] = {
            "target_mrr": t_mrr,
            "required_users": round(req_users, 1),
            "required_arr": round(t_mrr * 12, 2)
        }

    return {
        "model_type": "subscription",
        "currency": currency,
        "inputs": {
            "fixed_costs_monthly": fixed_costs,
            "variable_costs_per_user_monthly": variable_costs_per_user,
            "monthly_price": monthly_price,
            "monthly_churn_rate": f"{churn:.1%}",
            "margin_per_user": round(margin_per_user, 2),
            "margin_rate": f"{margin_rate:.1%}",
            "ltv_per_user": round(ltv, 2),
            "cac_per_user": cac,
            "cac_payback_months": round(cac / margin_per_user, 1) if cac > 0 and margin_per_user > 0 else None,
            "ltv_cac_ratio": round(ltv / cac, 1) if cac > 0 else None,
        },
        "breakeven": {
            "users": round(breakeven_users, 1),
            "mrr": round(breakeven_users * monthly_price, 2),
            "description": f"需要{round(breakeven_users, 1)}个付费用户，MRR达到{round(breakeven_users * monthly_price, 2)}{currency}即可盈亏平衡"
        },
        "scenarios": scenarios,
        "safety_margin": {
            "rate": f"{safety_margin:.1%}",
            "description": _safety_desc(safety_margin)
        },
        "profit_targets": targets,
        "recommendations": _generate_subscription_recommendations(margin_rate, safety_margin, breakeven_users, moderate, churn, ltv)
    }


def _safety_desc(rate):
    if rate > 0.5:
        return "较高安全边际，经营风险较低"
    elif rate > 0.2:
        return "中等安全边际，需关注波动"
    elif rate > 0:
        return "较低安全边际，建议降低成本或提高销量"
    else:
        return "负安全边际，中性预测下仍亏损，需调整定价或成本结构"


def _generate_recommendations(margin_rate, safety_margin, breakeven, moderate):
    recs = []
    if margin_rate < 0.3:
        recs.append("毛利率偏低(<30%)，建议提高定价或降低变动成本")
    elif margin_rate > 0.7:
        recs.append("毛利率优秀(>70%)，有空间进行促销获客")
    if breakeven > moderate * 0.8:
        recs.append("盈亏平衡点接近中性预测，经营风险较高，建议优先降低固定成本")
    if safety_margin < 0.2:
        recs.append("安全边际不足，建议: 1)降低固定成本 2)提高客单价 3)增加销售渠道")
    if moderate < 10:
        recs.append("中性月销量较低，建议先验证市场需求，从小规模测试开始")
    if not recs:
        recs.append("财务模型健康，建议按中性预测执行，持续监控实际数据与预测的偏差")
    return recs


def _generate_subscription_recommendations(margin_rate, safety_margin, breakeven, moderate, churn, ltv):
    recs = []
    if margin_rate < 0.5:
        recs.append("订阅毛利率偏低(<50%)，SaaS建议毛利率>70%，需优化成本结构或提高定价")
    elif margin_rate > 0.8:
        recs.append("订阅毛利率优秀(>80%)，可加大获客投入")
    if churn > 0.1:
        recs.append(f"月流失率{churn:.0%}偏高(>10%)，需重点提升留存: 优化产品价值、增加切换成本、建立社群")
    elif churn > 0.05:
        recs.append(f"月流失率{churn:.0%}中等(5-10%)，建议持续优化留存机制")
    else:
        recs.append(f"月流失率{churn:.0%}优秀(<5%)，产品粘性强")
    if ltv < 500:
        recs.append(f"LTV较低({round(ltv)}元)，建议: 1)降低流失率 2)提高客单价 3)增加增值服务")
    if breakeven > moderate * 0.8:
        recs.append("盈亏平衡用户数接近中性预测，建议降低固定成本或加速获客")
    if not recs:
        recs.append("订阅模型健康，建议聚焦获客和留存双轮驱动")
    return recs


def main():
    parser = argparse.ArgumentParser(
        description="全球一人公司创业全链路指导系统 - 财务模型计算器(支持一次性购买/订阅制/AI成本对比)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例(一次性购买):
  python scripts/financial_calculator.py --model one-time --fixed-costs 500 --variable-costs 20 --price 99 --conservative 30 --moderate 80 --optimistic 200

示例(订阅制/SaaS):
  python scripts/financial_calculator.py --model subscription --fixed-costs 2000 --variable-costs 10 --price 49 --conservative 50 --moderate 200 --optimistic 500 --churn 5

示例(AI成本对比):
  python scripts/financial_calculator.py --model compare
  python scripts/financial_calculator.py --model compare --traditional-low 30000 --traditional-high 50000 --ai-low 250 --ai-high 1000
        """
    )
    parser.add_argument("--model", type=str, default="one-time", choices=["one-time", "subscription", "compare"],
                        help="商业模型: one-time(一次性购买) / subscription(订阅制) / compare(AI成本对比)")
    parser.add_argument("--fixed-costs", type=float, default=0, help="月固定成本(元)")
    parser.add_argument("--variable-costs", type=float, default=0, help="单位变动成本/每用户月成本(元)")
    parser.add_argument("--price", type=float, default=0, help="单价/月费(元)")
    parser.add_argument("--conservative", type=int, default=0, help="保守预测(月销量或用户数)")
    parser.add_argument("--moderate", type=int, default=0, help="中性预测(月销量或用户数)")
    parser.add_argument("--optimistic", type=int, default=0, help="乐观预测(月销量或用户数)")
    parser.add_argument("--churn", type=float, default=5, help="月流失率%%(仅订阅制,默认5%%)")
    parser.add_argument("--cac", type=float, default=0, help="单用户获客成本(元,仅订阅制,用于计算CAC回本周期)")
    parser.add_argument("--traditional-low", type=float, default=30000, help="传统团队月成本下限(仅compare,默认30000)")
    parser.add_argument("--traditional-high", type=float, default=50000, help="传统团队月成本上限(仅compare,默认50000)")
    parser.add_argument("--ai-low", type=float, default=250, help="AI驱动月成本下限(仅compare,默认250)")
    parser.add_argument("--ai-high", type=float, default=1000, help="AI驱动月成本上限(仅compare,默认1000)")
    parser.add_argument("--currency", type=str, default="CNY", help="货币单位(默认CNY)")

    args = parser.parse_args()

    if args.model == "compare":
        result = calculate_compare_model(
            traditional_low=args.traditional_low,
            traditional_high=args.traditional_high,
            ai_low=args.ai_low,
            ai_high=args.ai_high,
            currency=args.currency if args.currency != "CNY" else "USD"
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.fixed_costs < 0:
        print(json.dumps({"error": "固定成本不能为负数"}, ensure_ascii=False))
        sys.exit(1)
    if args.variable_costs < 0:
        print(json.dumps({"error": "变动成本不能为负数"}, ensure_ascii=False))
        sys.exit(1)
    if args.price <= 0:
        print(json.dumps({"error": "单价必须大于0"}, ensure_ascii=False))
        sys.exit(1)

    if args.model == "subscription":
        result = calculate_subscription_model(
            fixed_costs=args.fixed_costs,
            variable_costs_per_user=args.variable_costs,
            monthly_price=args.price,
            conservative=args.conservative,
            moderate=args.moderate,
            optimistic=args.optimistic,
            monthly_churn_rate=args.churn,
            currency=args.currency,
            cac=args.cac
        )
    else:
        result = calculate_one_time_model(
            fixed_costs=args.fixed_costs,
            variable_costs=args.variable_costs,
            price=args.price,
            conservative=args.conservative,
            moderate=args.moderate,
            optimistic=args.optimistic,
            currency=args.currency
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if isinstance(result, dict) and "error" in result else 0)


if __name__ == "__main__":
    main()
