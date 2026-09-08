# Source provenance

Package refreshed on 8 September 2026; data snapshots unchanged. Original download dates were not consistently recorded; INPUT_SHA256.json identifies the exact files.

## Data and references used

| Source | Contribution to this presentation |
|:--|:--|
| [Observatoire de l’Habitat · advertised apartment rents](https://data.public.lu/fr/datasets/loyers-annonces-des-logements-par-commune/) | Annual commune averages and advertisement counts, 2009–2025. Local source: `loyers-apparts-2009-2025.xls`. |
| [STATEC · national CPI (IPCN), DF_E5401](https://lustat.statec.lu/vis?df[ds]=ds-release&df[ag]=LU1&df[id]=DSD_ECOICOP_PRIX@DF_E5401) | All-items monthly IPCN, 2009–2025, base 2015=100. Annual means of 12 observations; used to express purchasing power in 2025 euros. Local source: `ipcn_review_5401.csv`. |
| [Eurostat · yth_demo_030](https://ec.europa.eu/eurostat/databrowser/view/yth_demo_030/default/table?lang=en) | Estimated departure-age indicator, Luxembourg, both sexes: 26.6 in 2025 (26.9 in 2024). Local source: `leaving_home_eurostat.json`, updated 16 April 2026. |
| [STATEC · RP2021 n°17, Table 4, p. 8](https://statistiques.public.lu/dam-assets/catalogue-publications/rp-2021/rp17-jeunes/17-03-fr.pdf) | National household-position percentages by age in 2021. Sum of the three child categories: 78.6%, 37.7%, 13.1%. |
| [ACT · administrative boundaries](https://data.public.lu/fr/datasets/limites-administratives-du-grand-duche-de-luxembourg/) | Fixed 2023 geography: 100 communes. GeoJSON outlines simplified for the map; historical communes harmonised to this geography. |
| [LISER · Observatoire social de Schifflange, March 2023, pp. 62–63](https://schifflange.lu/wp-content/uploads/2023/04/Rapport-Observatoire-social-Schifflange-final-compressed.pdf#page=62) | Table 20: 246 social rental dwellings, based on Commune de Schifflange data for 2022; discussion of stock, dwelling types and demand. |
| [Gertler, Galiani & Romero · Nature (2018)](https://www.nature.com/articles/d41586-018-02108-9), [supplement, pp. 1–2](https://media.nature.com/original/magazine-assets/d41586-018-02108-9/gertler-et-al.-Comment-supplementary-information) | Reproducibility example: 14% of 203 sampled empirical papers fully reproducible from raw data to final exhibits. Contextual reference, not a housing dataset. |


[Presentation repository](https://github.com/hdbt/LISER-Presentation-A-place-of-your-own) · Local audit: `scripts/12_leaving_home.py`, `data/clean/rental_scenario.csv`, `data/clean/ipcn_annual.csv`. Other exploratory datasets in the project are not inputs to the findings shown here.



The rental dataset and ACT geometry were identified as CC0 in the original project. Consult linked provider terms for redistribution. Eurostat and STATEC retain their respective reuse conditions.
