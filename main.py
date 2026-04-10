import argparse
import sys
from loguru import logger
import os

def main():
    parser = argparse.ArgumentParser(description="SnailRouter 联合工作区总入口",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", help="可选用的子模块")

    # 1. 后端模型训练模块
    train_parser = subparsers.add_parser("train", help="训练后端模型 (如 DynaRouter Transformer变体)")
    train_parser.add_argument("--config", type=str, default="configs/exp_full.yaml", help="配置文件路径")
    train_parser.add_argument("--loss_type", type=str, default="pinball", choices=["mse", "ic", "pinball"], help="回归或分位数约束")
    train_parser.add_argument("--epochs", type=int, default=10, help="轮数")
    train_parser.add_argument("--batch_size", type=int, default=128, help="Batch Size")
    train_parser.add_argument("--use_dummy_data", action="store_true", help="使用虚拟数据快速测试")

    # 2. 模型评估回测模块
    eval_parser = subparsers.add_parser("eval", help="评估离线模型预测结果 (双轨校验与蜗牛壳指标)")
    eval_parser.add_argument("--pred_path", type=str, required=True, help="预测结果 CSV 路径")
    
    # 3. 树模型基线 (传统 snail-shell)
    compare_parser = subparsers.add_parser("compare", help="运行传统树模型对比 (XGBoost/CatBoost/LGBM 等) 测试 Snail-shell 核心效果")
    
    # 4. 在线预测
    predict_parser = subparsers.add_parser("predict", help="执行量化市场每日在线扫描预测")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "train":
        logger.info("启动 DynaRouter 后端大模型训练任务...")
        # 实际通过命令行调用 train.py 以维持多进程 GPU 参数解析纯净度，或者在脚本中导入 main 进行隔离执行
        cmd = f"python train.py --config {args.config} --loss_type {args.loss_type} --epochs {args.epochs} --batch_size {args.batch_size}"
        if args.use_dummy_data:
            cmd += " --use_dummy_data"
        os.system(cmd)

    elif args.command == "eval":
        logger.info(f"启动模型评估回测模块: 分析预测结果 {args.pred_path}")
        os.system(f"python evaluate.py --pred_path {args.pred_path}")

    elif args.command == "compare":
        logger.info("启动传统蜗牛壳树模型对比实验...")
        import main_snail
        # 委派给原 snail shell entry point
        # 此处待后期重构，目前先给出占位印记
        logger.warning("传统的对比脚本调用未完全重构接入命令树，这将在下一步完成整合。你也可以使用 python main_snail.py compare。")
        
    elif args.command == "predict":
        logger.info("启动每日预测任务...")
        # 可以整合 daily_predict
        logger.warning("每日预测系统这尚未完成对 DynaRouter 接口的数据源流校准。")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
