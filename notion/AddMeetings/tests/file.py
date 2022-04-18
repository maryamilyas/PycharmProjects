from notion.client import NotionClient

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="f81b9789f45500290b02e0320b363b5ff453f927d43d4f369717579026e4b93c5ac7b6ec45dd1f5038badc45d0a18d4c5472ad205de674a1568991f6da42c9343647fefdec749943f422195464f8")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/maryamilyas/42a936bef9224cfdbf0d366dd3b81587?v=43f497fd46ce4f8fa4aa6b2b1461db7a")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "The title has now changed, and has *live-updated* in the browser!"