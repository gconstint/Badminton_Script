"""
版本管理模块
自动获取 GitHub 上的最新 tag 作为版本号
"""

import subprocess
import re
import requests
from typing import Optional


class VersionManager:
    def __init__(self, fallback_version: str = "v3.0"):
        """
        初始化版本管理器
        
        Args:
            fallback_version: 当无法获取版本时的备用版本号
        """
        self.fallback_version = fallback_version
        self._cached_version = None
    
    def get_git_tag_version(self) -> Optional[str]:
        """
        从本地 Git 获取最新的 tag 版本
        
        Returns:
            最新的 tag 版本，如果失败返回 None
        """
        try:
            # 获取最新的 tag
            result = subprocess.run(
                ['git', 'describe', '--tags', '--abbrev=0'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                tag = result.stdout.strip()
                # 确保 tag 格式正确 (vX.X.X)
                if re.match(r'^v\d+\.\d+(\.\d+)?$', tag):
                    return tag
                    
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
            
        return None
    
    def get_github_latest_tag(self, repo_owner: str, repo_name: str) -> Optional[str]:
        """
        从 GitHub API 获取最新的 release tag
        
        Args:
            repo_owner: GitHub 仓库所有者
            repo_name: GitHub 仓库名称
            
        Returns:
            最新的 release tag，如果失败返回 None
        """
        try:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                tag = data.get('tag_name', '')
                # 确保 tag 格式正确
                if re.match(r'^v\d+\.\d+(\.\d+)?$', tag):
                    return tag
                    
        except (requests.RequestException, ValueError):
            pass
            
        return None
    
    def get_version(self, repo_owner: str = None, repo_name: str = None) -> str:
        """
        获取版本号，优先级：缓存 > Git tag > GitHub API > 备用版本
        
        Args:
            repo_owner: GitHub 仓库所有者（可选）
            repo_name: GitHub 仓库名称（可选）
            
        Returns:
            版本号字符串
        """
        # 如果已经缓存了版本，直接返回
        if self._cached_version:
            return self._cached_version
        
        # 1. 尝试从本地 Git 获取
        version = self.get_git_tag_version()
        if version:
            self._cached_version = version
            return version
        
        # 2. 如果提供了 GitHub 信息，尝试从 GitHub API 获取
        if repo_owner and repo_name:
            version = self.get_github_latest_tag(repo_owner, repo_name)
            if version:
                self._cached_version = version
                return version
        
        # 3. 使用备用版本
        self._cached_version = self.fallback_version
        return self.fallback_version
    
    def get_version_display(self, repo_owner: str = None, repo_name: str = None) -> str:
        """
        获取用于显示的版本号（去掉 'v' 前缀）
        
        Args:
            repo_owner: GitHub 仓库所有者（可选）
            repo_name: GitHub 仓库名称（可选）
            
        Returns:
            用于显示的版本号字符串
        """
        version = self.get_version(repo_owner, repo_name)
        # 去掉 'v' 前缀
        if version.startswith('v'):
            return version[1:]
        return version
    
    def refresh_version(self):
        """
        刷新版本缓存，强制重新获取版本号
        """
        self._cached_version = None
    
    def is_development_version(self) -> bool:
        """
        检查当前是否为开发版本（即使用了备用版本）
        
        Returns:
            如果是开发版本返回 True
        """
        return self._cached_version == self.fallback_version


# 创建全局版本管理器实例
version_manager = VersionManager()


def get_app_version(repo_owner: str = None, repo_name: str = None) -> str:
    """
    便捷函数：获取应用版本号
    
    Args:
        repo_owner: GitHub 仓库所有者（可选）
        repo_name: GitHub 仓库名称（可选）
        
    Returns:
        版本号字符串
    """
    return version_manager.get_version_display(repo_owner, repo_name)


if __name__ == "__main__":
    # 测试代码
    vm = VersionManager()
    print(f"Git tag version: {vm.get_git_tag_version()}")
    print(f"App version: {vm.get_version_display()}")
