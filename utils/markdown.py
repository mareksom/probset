from markdown import markdown
from pymdownx import emoji

extensions = [
    "markdown.extensions.tables",
    "pymdownx.magiclink",
    "pymdownx.betterem",
    "pymdownx.tilde",
    "pymdownx.emoji",
    "pymdownx.tasklist",
    "pymdownx.superfences",
    "pymdownx.saneheaders",
    "pymdownx.arithmatex",
]

extension_configs = {
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "social_url_shortener": True,
    },
    "pymdownx.tilde": {"subscript": False},
    "pymdownx.emoji": {
        "emoji_index": emoji.gemoji,
        "emoji_generator": emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {"align": "absmiddle", "height": "20px", "width": "20px"},
            "image_path": "https://github.githubassets.com/images/icons/emoji/unicode/",
            "non_standard_image_path": "https://gitfhub.githubassets.com/images/icons/emoji/",
        },
    },
    "pymdownx.arithmatex": {"generic": True},
    "pymdownx.superfences": {"css_class": "code"},
}


def evaluate(text):
    return (
        '<div class="markdown bbcode">'
        + markdown(text, extensions=extensions, extension_configs=extension_configs)
        + "</div>"
    )
