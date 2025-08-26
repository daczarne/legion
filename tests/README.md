# Current tests

The tables here describe the testing state that I wish to achieve (eventually). Each row in each table represents a
possible scenario of city configurations that "make sense" from the gameplay perspective. Checks marked with ✅ have
already been implemented. Other checks still need to be implemented.

## Cities without Warehouse or Supply Dump

| city focus | plain | lake  | lake + outcrop | outcrop | outcrop + mountain | mountain | mountains |
|:----------:|:-----:|:-----:|:--------------:|:-------:|:------------------:|:--------:|:---------:|
| food       |  ✅   |  ✅   |                |   ✅    |                    |          |           |
| ore        |  ✅   |       |                |   ✅    |         ✅         |    ✅    |    ✅     |
| wood       |  ✅   |       |                |         |                    |          |           |
| military   |  ✅   |       |                |         |                    |          |           |

## Cities with Warehouse

| city focus | plain | lake  | lake + outcrop | outcrop | outcrop + mountain | mountain | mountains |
|:----------:|:-----:|:-----:|:--------------:|:-------:|:------------------:|:--------:|:---------:|
| food       |       |       |                |         |                    |          |           |
| ore        |       |       |                |         |                    |          |           |
| wood       |       |       |                |         |                    |          |           |
| military   |       |       |                |         |                    |          |           |

## Cities with Supply Dump

Only the plain tests make sense since the cities with Supply Dump do not have any geo. features.

| city focus | plain | lake  | lake + outcrop | outcrop | outcrop + mountain | mountain | mountains |
|:----------:|:-----:|:-----:|:--------------:|:-------:|:------------------:|:--------:|:---------:|
| food       |  ✅   |  ➖   |       ➖       |   ➖    |         ➖         |    ➖    |    ➖     |
| ore        |       |  ➖   |       ➖       |   ➖    |         ➖         |    ➖    |    ➖     |
| wood       |       |  ➖   |       ➖       |   ➖    |         ➖         |    ➖    |    ➖     |
| military   |       |  ➖   |       ➖       |   ➖    |         ➖         |    ➖    |    ➖     |
