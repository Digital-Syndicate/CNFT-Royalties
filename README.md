# CNFT-Royalties
Repo for managing Cardano NFT Artist Royalties

This repo is managed and currated by Digital Syndicate.  Please make a pull request to have your project(s) added.

All royalties listed on this repo have been vetted for proper ownership, and contain reasonable royalties for the project they pertain to.
This repo can be considered a trusted source for CNFT Marketplaces to leverage for royalties distribution.

All royalties jsons must be in the latest standard format to be initially listed or updated.

Current Royalties Standard Version 0.1

The following tags are to be used for version 0.1

"royalties" - Placed within CNFT Metadata.  Can either be an array that contains the royalties instructions, or contains a link to offchain royalties json which includes the royalties instructions.  The link to an offchain json is recommended so that it can be modified in the future.

Royalties instructions tags:

"royaltiesContact": contact info for royalties inquiries (optional)
"royaltiesPercent": Overall percentage of resale to be distrubuted as royalties
"royaltiesPrimaryOwner": Friendly name of first royalties party (optional)
"royaltiesPrimaryPercent": Percentage of royalties distribution for the first party
"royaltiesPrimaryWallet": Wallet address to forward royalties to first party
"royaltiesSecondaryOwner": Friendly name of second royalties party (optional)
"royaltiesSecondaryPercent": Percentage of royalties distribution for the second party (optional)
"royaltiesSecondaryWallet": Wallet address to forward royalties to second party (optional)
"royaltiesTertiaryOwner": Friendly name of third royalties party (optional)
"royaltiesTertiaryPercent": Percentage of royalties distribution for the third party (optional)
"royaltiesTertiaryWallet": Wallet address to forward royalties to third party (optional)
"royaltiesQuaternaryOwner": Friendly name of fourth royalties party (optional)
"royaltiesQuaternaryPercent": Percentage of royalties distribution for the fourth party (optional)
"royaltiesQuaternaryWallet": Wallet address to forward royalties to fourth party (optional)



Examples of version 0.1 Royalties Configuration

Example within CNFT Metadata
"royalties": "https://bit.ly/3yToIri"

Example of JSON Placed on this repo

[{
	"royaltiesContact": "loa-royalties@digitialsyndicate.io",
	"royaltiesPercent": "10.0",
	"royaltiesPrimaryOwner": "Praga Khan",
	"royaltiesPrimaryPercent": "40.0",
	"royaltiesPrimaryWallet": "addr1v80gf3xn485sc9qea4keh99klqk70vhdd923c43kh3tud9g2gmu0w",
	"royaltiesSecondaryOwner": "Karl Kotas",
	"royaltiesSecondaryPercent": "40.0",
	"royaltiesSecondaryWallet": "addr1v98us4rxzjwxm0w0sl22u64tdw0c0vclufj2qwacgf5dcaqpn85q8",
	"royaltiesTertiaryOwner": "DigitalSyndicate",
	"royaltiesTertiaryPercent": "20.0",
	"royaltiesTertiaryWallet": "addr1vxjrmfpz9eh8ypps8yfh50snuk2e4q0ek60lxgcrt9y3tucxs2yfw"
}]
