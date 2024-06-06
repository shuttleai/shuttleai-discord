import json
import os
from typing import Any, Dict, List, Optional

import httpx
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.ticker import FormatStrFormatter

module_path = os.path.dirname(os.path.realpath(__file__))
package_path = os.path.dirname(module_path)
project_path = os.path.dirname(package_path)
cache_file = os.path.join(project_path, "etc", "cache", "contributors", "list.json")
avatars_cache_dir = os.path.join(project_path, "etc", "cache", "contributors", "avatars")

os.makedirs(avatars_cache_dir, exist_ok=True)

def load_cache() -> Optional[List[Dict[str, Any]]]:
    if os.path.exists(cache_file):
        with open(cache_file, "r") as file:
            return json.load(file)  # type: ignore
    return None

def save_cache(data: List[Dict[str, Any]]) -> None:
    with open(cache_file, "w") as file:
        json.dump(data, file)

def fetch_contributors() -> List[Dict[str, Any]]:
    url = "https://api.github.com/repos/shuttleai/shuttleai-python/contributors"
    cresponse = httpx.get(url, timeout=30, headers={"Accept": "application/json; charset=utf-8"})
    return cresponse.json()  # type: ignore

def main() -> None:
    cached_data = load_cache()

    usernames: List[str]
    contributions: List[int]
    avatars: List[str]

    if cached_data:
        cached_usernames = [contributor["login"] for contributor in cached_data]

        current_data = fetch_contributors()
        current_usernames = [contributor["login"] for contributor in current_data]

        if set(cached_usernames) == set(current_usernames):
            contributors = cached_data
        else:
            contributors = current_data
            save_cache(contributors)
    else:
        contributors = fetch_contributors()
        save_cache(contributors)

    usernames = [contributor["login"] for contributor in contributors]
    contributions = [contributor["contributions"] for contributor in contributors]
    avatars = [contributor["avatar_url"] for contributor in contributors]

    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor("#1e1e1e")
    ax.set_facecolor("#1e1e1e")

    bars = ax.barh(usernames, contributions, color="#7b1fa2", edgecolor="grey", height=0.6)
    ax.set_title("shuttleai-python Contributors", fontsize=24, fontweight="bold", color="white", pad=20)

    client = httpx.Client()
    for i, (username, avatar_url) in enumerate(zip(usernames, avatars)):
        avatar_path = os.path.join(avatars_cache_dir, f"{username}.png")
        if not os.path.exists(avatar_path):
            response = client.get(avatar_url, timeout=30, headers={"Accept": "image/*"})
            with open(avatar_path, "wb") as img_file:
                img_file.write(response.content)
        img = mpimg.imread(avatar_path)
        imagebox = OffsetImage(img, zoom=0.15, resample=True)
        ab = AnnotationBbox(imagebox, (-0.1, i), xycoords=("axes fraction", "data"),
        box_alignment=(1, 0.5), frameon=False, pad=0.5)
        ax.add_artist(ab)

    ax.set_xlim(left=-0.15, right=max(contributions) * 1.1)
    ax.invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.7, color="grey")
    plt.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)

    ax.xaxis.set_major_formatter(FormatStrFormatter("%d"))
    plt.xticks(fontsize=14, color="white")
    plt.yticks(fontsize=14, color="white")

    for i, v in enumerate(contributions):
        ax.text(v + 0.5, i, str(v), color="white", fontsize=12, va="center")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.tick_params(axis="both", length=0)

    for bar in bars:
        bar.set_alpha(0.8)
        bar.set_edgecolor("none")
        bar.set_zorder(1)

    ax.legend(["Contributions"], fontsize=14, facecolor="#1e1e1e", edgecolor="grey",
    labelcolor="white", loc="upper right", framealpha=0.8)

    plt.tight_layout()
    plt.show()
