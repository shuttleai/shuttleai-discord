import os
import shutil


def remove_pycache(root_dir: str = ".") -> None:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Removed {pycache_path}")
        for filename in filenames:
            if filename.endswith(".pyc") or filename.endswith(".pyo"):
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)
                print(f"Removed {file_path}")


def remove_mypy_cache(root_dir: str = ".") -> None:
    for dirpath, dirnames, _ in os.walk(root_dir):
        if ".mypy_cache" in dirnames:
            mypy_cache_path = os.path.join(dirpath, ".mypy_cache")
            shutil.rmtree(mypy_cache_path)
            print(f"Removed {mypy_cache_path}")


def remove_ruff_cache(root_dir: str = ".") -> None:
    for dirpath, dirnames, _ in os.walk(root_dir):
        if ".ruff_cache" in dirnames:
            ruff_cache_path = os.path.join(dirpath, ".ruff_cache")
            shutil.rmtree(ruff_cache_path)
            print(f"Removed {ruff_cache_path}")


def clean_all(root_dir: str = ".") -> None:
    remove_pycache(root_dir)
    remove_mypy_cache(root_dir)
    remove_ruff_cache(root_dir)
