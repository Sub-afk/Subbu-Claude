# AI's footprint, body-powered phones and living-cell computers: a learning guide

*Researched September 2026. Numbers change fast in these fields, so every major claim links to its
source so you can check it and go deeper.*

**Contents**
1. [Cutting AI's drinking-water use](#1-cutting-ais-drinking-water-use)
2. [Dealing with data-centre heat](#2-dealing-with-data-centre-heat)
3. [Keeping forests standing: siting and efficiency](#3-keeping-forests-standing-siting-and-efficiency)
4. [Charging a phone from your body or motion](#4-charging-a-phone-from-your-body-or-motion)
5. [Storing data in cells and computing with neurons (the "Sybil System" question)](#5-storing-data-in-cells-and-computing-with-neurons)
6. [How the pieces connect](#6-how-the-pieces-connect)
7. [Further reading](#7-further-reading)

---

## 1. Cutting AI's drinking-water use

### Why AI uses water at all
Chips turn almost all the electricity they use into heat. For years the cheapest way to remove
that heat was **evaporative cooling**: warm water flows over cooling towers and part of it
evaporates, carrying heat away, much like sweat cools skin. The evaporated water is *consumed*:
it doesn't come back to the local supply. It is often municipal drinking water, because
treated water doesn't clog the equipment.

There are three layers of water use, and arguments about AI's water footprint usually come down
to which layers each side counts:

| Layer | What it is | Who controls it |
|---|---|---|
| **Scope 1: on-site** | Evaporation in cooling towers, humidification | Data-centre operator |
| **Scope 2: electricity** | Water evaporated at the power plants (thermal and nuclear plants, hydro reservoirs) that supply the data centre | Grid mix |
| **Scope 3: supply chain** | Ultrapure water used to make chips (a large fab uses millions of litres a day) | Chipmakers |

### How big is it?
- Data centres worldwide consumed about **222 billion litres** of cooling water in 2025. Without
  changes that could reach about **644 billion litres by 2030**
  ([TechXplore, Sept 2026](https://techxplore.com/news/2026-09-ai-centers-thirsty-tech-giants.html)).
- **Per prompt, the estimates are far apart.** Google says a median Gemini text prompt uses about
  **0.26 mL** (roughly five drops) of water and 0.24 Wh of energy
  ([Google Cloud](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference)).
  UC Riverside's *Making AI Less Thirsty* study, which also counts water used to generate the
  electricity, estimated about 500 mL for a 20–50-message exchange with GPT-3-era models.
  Counting power-plant water raises per-prompt figures by roughly 2–3×
  ([PCWorld on the debate](https://www.pcworld.com/article/2886730/experts-are-skeptical-about-googles-ai-water-consumption-claims.html),
  [MDPI framework paper](https://www.mdpi.com/3042-9242/1/2/8)).
- **Location matters more than the global total.** A litre evaporated in rainy Finland is not a
  litre evaporated in drought-stressed Arizona or Chennai. Good analyses use *scarcity-weighted*
  water.

### The solutions, from most to least mature

**1. Closed-loop direct-to-chip liquid cooling (being deployed now).**
Coolant runs through cold plates bolted directly onto the GPUs, in a sealed loop that is filled
once. Heat leaves through dry coolers, which work like giant car radiators, instead of
evaporation.
- Microsoft's designs from August 2024 onward evaporate **zero water for cooling**. It says this
  saves more than 125 million litres per data centre per year. Pilots in Phoenix and Wisconsin
  start in 2026, and the design becomes standard from late 2027. Its fleet-wide water usage
  effectiveness (WUE) had already fallen from 0.49 to 0.30 L/kWh
  ([Microsoft](https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/12/09/sustainable-by-design-next-generation-datacenters-consume-zero-water-for-cooling/),
  [Microsoft 2026](https://blogs.microsoft.com/blog/2026/06/24/inside-microsofts-two-decade-push-to-cut-water-intensity-while-scaling-for-growth/)).
- Oracle and NVIDIA announced similar closed-loop, non-evaporative designs
  ([Oracle](https://www.oracle.com/news/announcement/blog/closed-loop-cooling-in-oracle-ai-data-centers-2026-02-09/)).
- **Warm-water cooling** is the key enabler. NVIDIA's newest racks accept coolant at about
  **45 °C**, so a plain radiator can cool the loop on most days of the year, even in hot climates,
  with no evaporation
  ([NVIDIA](https://blogs.nvidia.com/blog/liquid-cooling-ai-factories/)).

**2. Immersion cooling.** Whole servers sit in a non-conductive liquid. Single-phase immersion
circulates oil. Two-phase immersion boils a special fluid, which condenses and falls back. It
uses almost no water and captures heat well, but the fluids are expensive, some two-phase
fluids are PFAS ("forever chemicals"), and servicing hardware is harder.

**3. Non-potable water.** Where evaporation is still used, operators can switch to treated
wastewater (Google uses it in several sites), seawater (Google Hamina, Finland), or recycled
industrial water, so drinking water isn't used.

**4. Siting and scheduling ("follow the water").** Build in cool, water-rich places, and move
flexible workloads such as model training in time and space. Run them at night or in regions
where cooling is currently cheap. Research on geographic load balancing shows this can cut
water use and share its burden more fairly
([Li et al., arXiv](https://arxiv.org/pdf/2307.05494)).

**5. Cleaner electricity.** Because scope-2 water is often larger than on-site use, switching
from coal and gas to **wind and solar PV**, which use almost no water, cuts AI's total water
footprint substantially.

**6. Regulation.** More than 60 US state bills on data-centre water were introduced in 2025–26,
typically requiring water-use disclosure and closed-loop cooling in water-stressed areas
([Schneider Electric](https://blog.se.com/datacenter/2026/08/11/closed-loop-cooling-data-center-strategies-for-the-new-wave-of-u-s-state-water-rules/)).

> **The key trade-off:** evaporation is energy-efficient. Dry cooling uses more fan and chiller
> electricity on hot days, and electricity has its own water and carbon cost. Low water use and
> low energy use pull against each other, and the best designs (warm-water liquid cooling) avoid
> the trade-off by running hot enough that neither evaporation nor chillers are needed.

---

## 2. Dealing with data-centre heat

A quick physics point first: you can't destroy heat. The goals are to **(a) produce less** of it
(efficiency), **(b) put it to use** instead of dumping it, and **(c) avoid the emissions** that
come from making the electricity in the first place. Data-centre heat is a tiny share of global
warming directly. The real climate cost is the CO₂ from electricity generation.

### a) Produce less heat: efficiency
- **Better models and software.** Google reports that the energy per median Gemini prompt fell
  **33×** and its carbon **44×** in 12 months. The gains came from smaller "mixture-of-experts"
  models that activate only part of the network per query, speculative decoding, quantisation
  (using 8- or 4-bit numbers instead of 16-bit), better batching and newer chips
  ([Google Cloud](https://cloud.google.com/blog/products/infrastructure/measuring-the-environmental-impact-of-ai-inference)).
  Caveat: total AI use is growing faster than efficiency is improving. Cheaper queries lead to
  more queries (the **Jevons paradox**).
- **Right-size the model.** Many tasks don't need a frontier model. Routing easy requests to small
  models, or running them on the device (phone NPUs), avoids data-centre energy entirely.
- **Specialised chips** (TPUs, inference ASICs) do far more operations per watt than
  general-purpose GPUs.

### b) Put the heat to use
Liquid-cooled AI racks give off heat at **55–65 °C**, which is hot enough to feed district heating
networks directly
([ModulEdge](https://www.moduledge.com/blog/data-center-waste-heat-recovery),
[ScienceDirect review](https://www.sciencedirect.com/science/article/pii/S1364032125005362)).
Air-cooled halls gave off only 25–35 °C, which needed heat pumps to be useful. This is why the
switch to liquid cooling solves the water and heat problems together.

**Real examples**
- **Finland**: Microsoft and the energy company Fortum are building data centres whose heat will
  go to the Espoo/Helsinki district network, covering about 250,000 users. Google's Hamina site
  also exports heat.
- **Denmark**: Meta's Odense data centre heats more than 11,000 homes.
- **Stockholm Data Parks** buys heat from data centres for the city network.
- **Smaller scale**: swimming pools (Deep Green, UK), greenhouses and fish farms, and
  timber/food drying.

**Regulation is making this mandatory.** Germany's Energy Efficiency Act requires new data
centres (from July 2026) to reuse 10% of their heat, rising to 20% by 2028
([Vela Solaris](https://www.velasolaris.com/en/data-center-heat-reuse/)). The EU's Energy
Efficiency Directive requires large sites to report heat reuse, and some Nordic municipalities
won't grant permits without it.

**Why it isn't everywhere:** heat is hard to transport (pipes lose it and cost about €1–3M/km), the
heat is needed in winter while AI runs all year, and many data centres are built far from towns.
Solutions include seasonal thermal storage, district-cooling-plus-heating networks, and
**siting data centres next to heat users** from day one.

### c) Avoid emissions at the source
- 24/7 carbon-free electricity matching (hour by hour, not annual offsets), geothermal, nuclear
  (including small modular reactors, SMRs), and batteries.
- **Carbon-aware computing**: shift flexible jobs to hours when the grid is clean.
- **Heat-to-power** from low-grade heat (organic Rankine cycles) is technically possible, but at
  55–65 °C the efficiency is only a few percent, so direct heat reuse is almost always better.

---

## 3. Keeping forests standing: siting and efficiency

### The problem
Hyperscale campuses need hundreds to thousands of acres, plus land for transmission lines,
substations and roads. JLL expects about **100 GW** of new capacity worldwide between 2026 and
2030 ([Build.inc](https://build.inc/insights/data-center-brownfield-redevelopment)). In Virginia,
the proposed **2,100-acre PW Digital Gateway** would have cleared large areas of forest next to a
national battlefield park. After years of litigation the project collapsed in 2026, which shows
that community opposition over forests and land can stop projects
([DCD](https://www.datacenterdynamics.com/en/news/prince-william-county-environment-report-recommend-ditching-2000-acre-data-center-plans/),
[InsideNoVA](https://www.insidenova.com/news/prince_william/update-digital-gateway-data-center-project-dies-after-final-developer-drops-appeal/article_54179299-2733-4b4d-8fef-db4024cc8f54.html)).

### Solutions

**1. Build on land that's already been cleared.** This is the biggest lever.
- The US has about **500,000 brownfield sites (about 5 million acres)**: old factories, mines,
  retired coal plants. Coal-plant sites are especially attractive because they come with grid
  connections, water rights and industrial zoning. In January 2026 the EPA published guidance for
  building AI data centres on brownfield and Superfund sites
  ([EPA](https://www.epa.gov/brownfields/reuse-considerations-data-centers-brownfield-sites),
  [NLC](https://www.nlc.org/article/2026/03/31/understanding-epas-reuse-considerations-for-data-centers-on-brownfield-and-superfund-sites/)).
- Retrofit empty malls, warehouses and office buildings.

**2. Build up and pack it in.** Liquid cooling allows **100+ kW per rack**, compared with about
10 kW for air-cooled racks, so the same compute fits in a fraction of the floor space. Multi-storey
data centres are common in Singapore, Tokyo and Frankfurt, where land is expensive.

**3. Make the hardware do more ("optimise the devices").** Each efficiency gain means fewer
buildings for the same service:
- More work per watt and per square metre: newer chip generations, sparsity, low-precision math.
- **Extend hardware life and reuse parts.** Microsoft's "Circular Centers" aim to reuse or recycle about
  90% of server parts. Old accelerators can move down to simpler inference tasks.
- **Higher utilisation**: many private servers sit idle most of the time, and pooling in shared
  clouds cuts total hardware.
- **Edge and on-device AI**: small models on phones and laptops (NPUs) use hardware people already
  own.

**4. Timber, with a caveat.** Microsoft builds hybrid data centres with **cross-laminated
timber**, which cuts embodied carbon by 35% compared with steel and 65% compared with precast
concrete ([Microsoft](https://news.microsoft.com/source/features/sustainability/microsoft-builds-first-datacenters-with-wood-to-slash-carbon-emissions/)).
This *does* use trees, but from certified, replanted production forests, and it stores carbon in
the building. The goal is *no clearing of natural forest*, not zero wood.

**5. Policy tools.** Zoning that steers data centres to industrial land, "no net loss" of
tree-canopy rules, mandatory environmental impact assessments, and requirements to replant or
protect an equal area of forest elsewhere.

**6. Unusual sites.** Underwater pods (Microsoft's Project Natick found them *more* reliable),
floating barges, underground bunkers and old mines (Lefdal, Norway). Orbital data centres are
being studied, but they are far from practical.

---

## 4. Charging a phone from your body or motion

### The physics first
A modern phone battery holds about **5,000 mAh × 3.85 V ≈ 19 Wh ≈ 69,000 joules**. A phone uses
roughly **0.5–2 W** in active use and about 20–50 mW on standby. Whether a harvester is useful
depends on how many joules it can deliver per day.

| Energy source | What you can realistically harvest | Time to fully charge a 19 Wh phone |
|---|---|---|
| **Body as an antenna** (collecting ambient radio waves; your body's own electric field is far too weak to use) | ~0.6 µW outdoors ([PMC 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12349321/)) | ~3,500 **years** |
| **Body heat** (thermoelectric wristband, ΔT of a few °C) | ~0.1–1 mW for a band-sized device | ~2–20 **years** |
| **Phone-in-pocket motion** (tiny internal mass or coil generator, like an automatic watch) | ~1–10 mW while walking | ~3 months to 2 years |
| **Triboelectric fabrics / shoe insoles** (TENG: static-electricity generators) | ~1–50 mW while walking | ~2 weeks to 2 years |
| **Knee-brace generator** (captures the braking phase of walking) | ~**5 W** ([ScienceDaily 2008](https://www.sciencedaily.com/releases/2008/02/080207140751.htm)) | ~4–5 hours of walking |
| **Hand crank / pedal** | 5–20 W | about 1–4 hours |

### What this means
- **Your body's own electric and magnetic fields can't charge a phone.** Nerve and heart signals
  are micro- to millivolts at tiny currents, and the magnetic field of your brain is about a
  billionth of Earth's. Almost all of the body's roughly 100 W metabolism leaves as heat. The
  "human body antenna" research above is real, but it works by collecting *ambient radio waves*,
  and it produces well under a microwatt.
- **An automatic watch works because it needs almost nothing.** A mechanical or quartz watch
  movement uses about **1 µW**. A phone needs roughly **a million times more** (about 1 W).
  Wrist motion gives about a milliwatt, which is plenty for a watch and far too little for a
  phone.
- **Where harvesting works today:** watches (Seiko Kinetic, Citizen Eco-Drive light-powered),
  fitness bands and medical sensors with **thermoelectric** or **triboelectric** harvesters,
  self-powered IoT sensors, and **battery-free** Bluetooth tags. Research on body heat plus motion
  aims to *remove batteries from wearables* rather than from phones
  ([ScienceDirect review](https://www.sciencedirect.com/science/article/pii/S2211467X23000743)).
- **What could work for phones:**
  1. **Top-up rather than full charge.** Harvesting even 5–10% a day could matter for people
     without reliable power, for example in rural or disaster settings.
  2. **Harvesters on big muscles**, such as knee or backpack generators, where the watts actually
     are. They're used in military research for soldiers carrying battery packs.
  3. **Solar**: a phone-sized solar panel in sunlight gives about 1–2 W, which is 100–1,000× more
     than body harvesting. Solar backs and cases are the most practical "self-charging" route.
  4. **Lower-power phones.** Efficient displays (e-ink, LTPO) and chips shrink the demand side, so
     harvesters can cover more of it.

> **In short:** "charging like an automatic watch" is excellent for devices that need microwatts,
> and the approach is spreading through wearables and medical implants. For a phone it can only
> ever be a trickle top-up, unless you wear a generator on a big joint.

---

## 5. Storing data in cells and computing with neurons

There are three related but different ideas here, often mixed together:

### a) DNA data storage (DNA as a storage medium, no living cells needed)
- **Why it's appealing:** DNA is extremely dense. In theory about **215 petabytes fit in one
  gram**, and all of the world's data would fit in a few shoeboxes. Kept cool and dry it lasts
  thousands of years (we read DNA from mammoths), and we'll always have machines that can read it.
- **How it works:** convert bits to the bases A/C/G/T (for example 00→A, 01→C), synthesise the
  strands, dry them and store them. To read the data, sequence the DNA and decode it with heavy
  error correction.
- **Where it is in 2026:** the first commercial *archival* products exist. For example,
  **Biomemory** (France) sells "DNA Cards", and Atlas Data Storage is partnering with imec to scale
  up synthesis on chips
  ([GMI summary](https://www.gminsights.com/industry-analysis/dna-data-storage-market)).
  The main bottlenecks are **cost and write speed**: writing costs far more per gigabyte than tape,
  and it takes hours to days. It's suited to "write once, read almost never" archives such as film
  studios, national archives and scientific data, not everyday storage.

### b) Recording data inside living cells
Scientists use **CRISPR** as a biological tape recorder, writing information into the genomes of
living bacteria:
- In 2017 Harvard's Shipman and Church encoded a **short film of a galloping horse** into *E. coli*
  DNA and read it back
  ([Nature 2017](https://www.nature.com/articles/nature23017)).
- **DRIVES** (2021) wrote data into bacteria using **electrical signals**, which links electronics
  to living memory (72 bits)
  ([Nature Chem Bio](https://www.nature.com/articles/s41589-020-00711-4)).
- **Molecular recorders** such as DOMINO and CAMERA record *events* in human and bacterial cells,
  such as which signals a cell saw and when, onto its own DNA
  ([Nature 2022](https://www.nature.com/articles/s41586-022-04922-8)).
- The practical use is **medical and scientific, not IT storage**: cells that record what happened
  inside your gut, a tumour or a developing embryo. Living cells mutate and divide, so they are a
  poor medium for reliable bulk storage.

### c) Computing with living neurons: "organoid intelligence" and wetware
This is the part closest to your Sybil System idea.
- **What it is:** human stem cells (reprogrammed from skin or blood cells) grown into neurons or
  3D brain **organoids**, pea-sized clusters of up to millions of neurons, on top of
  **multi-electrode arrays**. The electrodes stimulate the neurons (input) and record their spikes
  (output), and the network adapts, so it learns.
- **Why:** the human brain runs on about **20 W**. Matching its ability in silicon takes megawatts.
  If even a fraction of that efficiency can be harnessed, it would ease AI's energy, water and heat
  problems.
- **Where it is in 2026:**
  - **Cortical Labs** (Melbourne): its 2022 "DishBrain" learned to play **Pong**. In 2025 it
    launched the **CL1**, a "code-deployable biological computer" with human neurons on a silicon
    chip, costing about **$35,000**, with remote cloud access. The CL1 has since been reported
    running DOOM.
  - **FinalSpark** (Switzerland): the **Neuroplatform**, 16 brain organoids that researchers can
    rent over the internet 24/7 through a Python API. It claims about a million times less energy
    per operation than digital chips, though that's measured on very simple tasks
    ([FinalSpark](https://finalspark.com/neuroplatform/),
    [ScienceAlert](https://www.sciencealert.com/computers-made-from-human-brain-tissue-are-coming-are-we-prepared),
    [MedicalXpress 2026](https://medicalxpress.com/news/2026-05-lab-grown-brain-organoids-power-biocomputers.html)).
  - **Johns Hopkins** (Thomas Hartung's team) coined "organoid intelligence" and leads the academic
    roadmap
    ([Frontiers 2023](https://www.frontiersin.org/journals/science/articles/10.3389/fsci.2023.1068159/full)).
- **Honest limits:** organoids live for months, not years. They have no blood vessels, so there
  are nutrient limits on their size. They are noisy and hard to reproduce, and the tasks they
  solve today, like Pong and simple pattern recognition, are toy-sized. Expect useful
  hybrid bio-silicon systems for **drug testing and neuroscience** this decade. General-purpose
  "wetware AI" is much further off, if it arrives at all.

### d) Psycho-Pass's Sybil System compared with reality
In *Psycho-Pass*, the Sybil System looks like an all-knowing machine. It is secretly a network
of about 200 human brains that governs society by scanning everyone's "Psycho-Pass" (mental
state) and predicting who will commit crimes.

| Sybil System element | Real-world counterpart | Status |
|---|---|---|
| Brains networked as a computer | Organoid intelligence, brain-on-chip | Early research. Thousands to millions of neurons, not whole brains |
| Reading mental states from a distance | EEG, fMRI decoding, brain-computer interfaces (Neuralink, Synchron, Paradromics) | BCIs decode movement or speech intent *with implanted electrodes or a scanner*. Remote mind-scanning isn't physically possible with known tech |
| "Crime coefficient" prediction | Predictive policing, risk-scoring algorithms, emotion recognition | **This part exists today**, and it's the real warning from the show |
| Society deferring to an opaque system | Automated decisions in welfare, credit and hiring | Being debated now (EU AI Act bans social scoring and most emotion recognition at work and school) |

**The ethical questions are already being asked:**
- **Could an organoid become conscious or feel pain?** There's no agreed test. The **Baltimore
  Declaration** (2023) calls for "embedded ethics", meaning ethicists involved from the start of
  organoid-intelligence research
  ([Springer review](https://link.springer.com/article/10.1007/s40778-025-00251-4),
  [Scientific Reports 2026](https://www.nature.com/articles/s41598-026-43243-y)).
- **Donor consent:** did the person whose cells grew the organoid agree to it being used as a
  computer?
- **Neurorights:** Chile wrote mental privacy into its constitution (2021), and Colorado and
  California protect neural data (2024). UNESCO adopted a global recommendation on the ethics of
  neurotechnology in 2025.

> **The takeaway:** the Sybil-like future to watch for isn't jars of brains. It's opaque
> algorithms given authority over people, combined with neural data collected by consumer
> devices. The biology is fascinating and moving fast, but the governance question is urgent
> right now.

---

## 6. How the pieces connect

```
          efficiency (models, chips, on-device AI)
                      │ fewer watts
                      ▼
   less heat ──► less cooling ──► less water ──► fewer/smaller buildings ──► less land cleared
                      │
          liquid cooling (hot, 45–65 °C)
            ├── no evaporation  → water solved
            ├── useful heat     → district heating
            └── dense racks     → smaller footprint
                      │
   long-term wildcards: biocomputing (brain-level efficiency), DNA archival storage (tiny footprint)
```

**One idea runs through all of it: energy efficiency.** Every watt not used removes a watt of
heat, a share of cooling water, a slice of power-plant emissions and a bit of building footprint.

---

## 7. Further reading

**Water and heat**
- Li, Yang, Islam, Ren, *Making AI Less Thirsty* (UC Riverside): the paper that started the debate
- Google, *Measuring the environmental impact of AI inference* ([arXiv 2508.15734](https://arxiv.org/pdf/2508.15734))
- IEA, *Energy and AI* report (2025): the global reference for data-centre electricity
- NYSERDA, [*DATA HEAT: Sector coupling of data centers and district heating* (2026)](https://www.nyserda.ny.gov/-/media/Project/Nyserda/Files/Programs/Large-Scale-Thermal/DATA-HEAT---Sector-Coupling-Data-Centers-and-District-Energy.pdf)

**Land**
- US EPA, [*Guidance on redevelopment of Superfund and brownfield sites as AI data centers* (Jan 2026)](https://www.epa.gov/system/files/documents/2026-01/guidance-on-the-redevelopment-of-superfund-and-brownfield-sites-as-ai-data-centers.pdf)

**Energy harvesting**
- Donelan et al., "Biomechanical energy harvesting", *Science* (2008): the knee-brace paper
- Zhong Lin Wang's group (Georgia Tech): the originators of triboelectric nanogenerators

**Biocomputing and DNA storage**
- Smirnova et al., "Organoid intelligence (OI): the new frontier in biocomputing", *Frontiers in Science* (2023)
- Kagan et al., "In vitro neurons learn and exhibit sentience when embodied in a simulated game-world" (DishBrain), *Neuron* (2022)
- Ceze, Nivala, Strauss, "Molecular digital data storage using DNA", *Nature Reviews Genetics* (2019)
- Shipman et al., "CRISPR–Cas encoding of a digital movie into the genomes of a population of living bacteria", *Nature* (2017)

*Note on sources: market-size forecasts for DNA storage vary by 100× between report vendors and
are left out on purpose. Corporate water and energy figures are self-reported, so compare them
with independent studies where you can.*
