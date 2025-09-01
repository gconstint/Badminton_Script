#!/usr/bin/env python3
"""
测试版本管理功能
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.version_manager import VersionManager, get_app_version
import version_config

def test_version_manager():
    """测试版本管理器的各种功能"""
    print("=== 版本管理器测试 ===")
    
    vm = VersionManager()
    
    # 测试 Git tag 获取
    git_version = vm.get_git_tag_version()
    print(f"Git tag 版本: {git_version}")
    
    # 测试 GitHub API 获取（如果配置了仓库信息）
    if hasattr(version_config, 'GITHUB_REPO_OWNER') and hasattr(version_config, 'GITHUB_REPO_NAME'):
        github_version = vm.get_github_latest_tag(
            version_config.GITHUB_REPO_OWNER, 
            version_config.GITHUB_REPO_NAME
        )
        print(f"GitHub API 版本: {github_version}")
    
    # 测试最终版本获取
    final_version = vm.get_version(
        version_config.GITHUB_REPO_OWNER if hasattr(version_config, 'GITHUB_REPO_OWNER') else None,
        version_config.GITHUB_REPO_NAME if hasattr(version_config, 'GITHUB_REPO_NAME') else None
    )
    print(f"最终版本: {final_version}")
    
    # 测试显示版本
    display_version = vm.get_version_display(
        version_config.GITHUB_REPO_OWNER if hasattr(version_config, 'GITHUB_REPO_OWNER') else None,
        version_config.GITHUB_REPO_NAME if hasattr(version_config, 'GITHUB_REPO_NAME') else None
    )
    print(f"显示版本: {display_version}")
    
    # 测试便捷函数
    app_version = get_app_version(
        version_config.GITHUB_REPO_OWNER if hasattr(version_config, 'GITHUB_REPO_OWNER') else None,
        version_config.GITHUB_REPO_NAME if hasattr(version_config, 'GITHUB_REPO_NAME') else None
    )
    print(f"应用版本: {app_version}")
    
    # 测试窗口标题
    if hasattr(version_config, 'APP_NAME'):
        window_title = f"{version_config.APP_NAME} V{app_version}"
        print(f"窗口标题: {window_title}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_version_manager()
