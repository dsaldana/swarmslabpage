# Google Scholar publication import

Checked **November 8, 2026**, from [David Saldaña’s Google Scholar profile](https://scholar.google.com/citations?user=VU1s_Z8AAAAJ).

The fetched profile contains **57 entries**, with the “Show more” button disabled. All 57 are mapped in `coverage.json`: **56 distinct works**, with one duplicate chapter consolidated. The site retains the original website-only paper *Toward Fine Contact Interactions: Learning to Control Normal Contact Force with Limited Information*. Result: **57 publication records, including 19 additions**.

## Additions

| Year | Work | Type |
| --- | --- | --- |
| 2026 | [From Hitch to Lift: Autonomous Cable Interlacing by Multi-UAV Teams for Aerial Grasping and Transportation](https://doi.org/10.1109/tro.2026.3677011) | Journal article |
| 2025 | [AirBender: Adaptive Transportation of Bendable Objects Using Dual UAVs](https://doi.org/10.1109/lra.2025.3536276) | Journal article |
| 2025 | [Decentralized Adaptive Aerospace Transportation of Unknown Loads Using A Team of Robots](https://doi.org/10.1007/978-3-032-04584-3_3) | Book chapter |
| 2025 | [FlySurf: A Flying Robotic Surface with Shape Morphing Control](https://doi.org/10.23919/acc63710.2025.11107545) | Conference paper |
| 2025 | [FlySurf: A Flying Robotic Surface with Shape Morphing and Motion Control](https://digitalrepository.unm.edu/ece_etds/730/) | Master’s thesis |
| 2025 | [Modular Multirotors: From Quadrotors to Fully-Actuated Aerial Vehicles](https://doi.org/10.1109/tase.2025.3594579) | Journal article |
| 2025 | [Reconfigurable Systems](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=VU1s_Z8AAAAJ&citation_for_view=VU1s_Z8AAAAJ:sNmaIFBj_lkC) | Book chapter |
| 2025 | [quasi-Dynamic Crowd Vetting: Collaborative Detection of Malicious Robots in Dynamic Communication Networks](https://doi.org/10.1109/tro.2025.3608702) | Journal article |
| 2024 | [KT-Imitation: Efficient Visual Imitation for Autonomous Navigation Based on Keypoint Timeline](https://doi.org/10.1109/lars64411.2024.10786409) | Conference paper |
| 2024 | [Rotor Fault Detection and Isolation in Aerial Vehicles with Dozens of Rotors](https://doi.org/10.1109/lars64411.2024.10786448) | Conference paper |
| 2023 | [A Novel Low-Cost, Recyclable, Easy-to-Build Robot Blimp For Transporting Supplies in Hard-to-Reach Locations](https://doi.org/10.1109/ghtc56179.2023.10355047) | Conference paper |
| 2023 | [Dynamic Crowd Vetting: Collaborative Detection of Malicious Robots in Dynamic Communication Networks](https://doi.org/10.1109/cdc49753.2023.10383774) | Conference paper |
| 2023 | [Learning to Navigate in Turbulent Flows With Aerial Robot Swarms: A Cooperative Deep Reinforcement Learning Approach](https://doi.org/10.1109/lra.2023.3280806) | Journal article |
| 2022 | [Adaptive Malicious Robot Detection in Dynamic Topologies](https://doi.org/10.1109/cdc51059.2022.9993343) | Conference paper |
| 2022 | [Customizable-ModQuad: a Versatile Hardware-Software Platform to Develop Lightweight and Low-cost Aerial Vehicles](https://www.researchgate.net/publication/368390753_Customizable-ModQuad_a_Versatile_Hardware-Software_Platform_to_Develop_Lightweight_and_Low-cost_Aerial_Vehicles) | Workshop extended abstract |
| 2022 | [Planning for Modular Aerial Robotic Tools with Temporal Logic Constraints](https://doi.org/10.1109/cdc51059.2022.9993288) | Conference paper |
| 2015 | [Y-Rescue Team Description Paper](https://cdn.robocup.org/rsim/public/competitions/2015-RSL/info/agent/rsl15-tdp-agent-Y-Rescue.pdf) | Team description paper |
| 2012 | [A multi-agent model to control robotic sensor networks](https://doi.org/10.1109/colombiancc.2012.6398036) | Conference paper |
| 2012 | [Improved algorithm for perimeter tracking in robotic sensor networks](https://doi.org/10.1109/clei.2012.6427231) | Conference paper |

## Reconciliation decisions

- **DARS chapter:** Scholar IDs `_5tno0g5mFcC` (full title, 2024) and `6ZxmRoH8BuwC` (truncated title, 2025) describe the same chapter, *Decentralized Adaptive Aerospace Transportation of Unknown Loads Using a Team of Robots*. The [publisher metadata](https://api.crossref.org/works/10.1007/978-3-032-04584-3_3) gives online publication on November 2, 2025, print volume year 2026, and pages 28–41. The site uses 2025, retains the [2024 preprint](https://arxiv.org/abs/2407.08084), and records both Scholar IDs.
- **FlySurf thesis:** The [UNM repository](https://digitalrepository.unm.edu/ece_etds/730/) identifies Kevin Aubert De Luchi Lomellini as the sole author of the 2025 master’s thesis. David Saldaña is a committee member. It is included because it appears on the requested profile, explicitly labeled as a thesis and distinct from the three-author ACC paper. David is not added to its author list.
- **Undated records:** Customizable-ModQuad is a 2022 workshop extended abstract according to [Lehigh AIRLab](https://wordpress.lehigh.edu/robotics/2023/01/30/latest-papers-to-appear-in-top-conferences-2023/). Y-Rescue is a 2015 team description paper; full author order comes from the [official RoboCup PDF](https://cdn.robocup.org/rsim/public/competitions/2015-RSL/info/agent/rsl15-tdp-agent-Y-Rescue.pdf). Neither is mislabeled as a full conference paper.
- **Reconfigurable Systems:** Title-only Crossref search returned an unrelated chapter. That match was rejected. Authors and 2025 publication details instead follow [UPenn ModLab’s bibliography](https://www.modlabupenn.org/publications/) and Springer’s encyclopedia listing. No DOI was invented.
- **SBlimp correction:** [arXiv](https://arxiv.org/abs/2308.00259) and the [first author’s publication list](https://www.jiawei-xu.dev/) place Diego S. D’Antonio second and Dominic J. Ammirato third. Corrected the WordPress author-order error and added the verified conference DOI; displayed and BibTeX author order agree.
- **Year differences:** Retained 2019 for *Design Guarantees for Resilient Robot Formations on Lattices* and 2015 for *Searching for Regions Out of Normal Conditions Using a Team of Robots*, matching publisher metadata rather than Scholar’s earlier years. Added the latter’s DOI and corrected its type to book chapter.
- **Version distinctions:** The 2023 CDC and 2025 T-RO Crowd Vetting papers have distinct titles/DOIs and remain separate. AirBender uses its 2025 RA-L publication year, not its later arXiv deposit year.

## Preservation and provenance

All 38 original files, abstracts, and PDF/video resources are retained. Full verified author lists are used instead of Scholar’s truncated lines. Existing file slugs remain stable. No citation counts are presented as live values.

- `profile.html`: original response (ISO-8859-1 encoding).
- `profile.json`: parsed complete profile, source URL, date, and pagination-completeness evidence.
- `existing-before.json`: immutable snapshot of the 38 pre-import records.
- `reviewed-metadata.json`: accepted metadata and primary-source URLs; no automatic title-only import.
- `ambiguity-evidence.json`: detailed decisions for the duplicate, thesis, undated works, and SBlimp correction.
- `crossref/`: primary publisher-deposited metadata and query evidence. Query candidates include rejected matches; accepted records are identified in `reviewed-metadata.json`.
- `coverage.json`: every Scholar ID mapped to its site Markdown file, including both IDs for the merged chapter.

Scholar’s detail endpoint returned a verification page, so full metadata was verified through publisher/Crossref records, author/lab publication pages, the UNM repository, and the official RoboCup paper. The complete profile list itself was successfully retrieved directly from Scholar. No authentication or verification challenge was bypassed.

`python3 scripts/import-scholar.py` reapplies this reviewed local snapshot; it is not a live scraper. For normal maintenance, edit the Markdown records. New import snapshots should be reviewed before replacing the evidence files.

## Validation

- `npm run check`: no Astro/TypeScript errors or warnings.
- `npm run build`: successful static build.
- `npm run check:site`: 47 pages, 57 publications, and 1,336 internal link/media references pass.
- `npm run check:scholar`: every one of the 57 Scholar IDs appears exactly once, duplicate DOI/ID checks pass, all original records/resources/abstracts survive, and thesis attribution and SBlimp BibTeX agree with the verified metadata.

The changes remain local; no deployment or changes to the live WordPress website were performed.
