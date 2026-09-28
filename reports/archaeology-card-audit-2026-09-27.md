# Storybook artifact-card audit against the archaeology records

## Verified by hand, 2026-09-27 (Claude, sources read directly)

The machine-generated audit below overreached. Cisco challenged it; these are the verdicts after
reading the primary and named sources myself. Where a card was fixed, the fix is applied in
`data/artifacts.json` / `data/chapters/ark-design.json` in the same commit.

| Card | Audit said | What the sources show | Action |
|---|---|---|---|
| mesha-stele | "[C] no 2023 imaging exists" | RTI photographs (USC WSRP, 2015) published by Lemaire & Delorme, *BAR* 48 (Nov 2022; press Jan 2023): "we believe the reading btdwd is confirmed once and for all." Richelle & Burlingame (*BAR* 2023; BAS 25 Aug 2023): the taw shows "only striations and small depressions"; still a hypothesis. | Card reworded as a named dispute, not a non-existent study. Audit was wrong. |
| tel-dan-stele | reading depends on the fragment join | Langlois (IEJ 74/2, 2024): "the new analysis doesn't change anything about the reading of the 'House of David' phrase." Only the restored royal names depend on the join. | No change. Audit was wrong. |
| soleb-yhw | "[C] last sign disputed" | Kennedy (Dotawo 6, 2019, p. 184): the report's G43 (w) "was a mistake, and the sign is clearly the G1 falcon representing aleph." The letters y-h-w are read the same by every editor. | Status reworded to say exactly that. Not a contradiction. |
| jeremiah-bullae | "[C] not in the 586 layer" | Mazar's own report (summarised by the Armstrong Institute): "Directly under the Babylonian stratum was the thick destruction layer corresponding to the fall of Jerusalem. This layer included the bulla of ... Gedaliah." Mykytiuk (2009: 94) notes the context's date is disputed and dates by letter forms to the same years. | Card now gives both: excavator's stratigraphy and the caution. |
| hezekiah-bulla | "[C] found 2015" | Excavated 2009 (Ophel, Area A), identified in wet-sifting, announced Dec 2015. | Precision fix applied. Not a contradiction. |
| pool-of-bethesda | "[C] porticoes never found" | Excavation exposed two basins divided by a dam (the five-sided plan); the colonnades themselves did not survive (PEF 1888 argued from John 5:2; von Wahlde, BAR 2011; BAS). | Card reworded: plan found, colonnades not. Overstatement, not contradiction. |
| mt-ebal-altar | critics only | IEJ 73/2 (Maeir & Rollston; Mazar; Yahalom-Mack) and Haughwout 2024 stand; so do Stripling & van der Veen (Mar 2024) and Stripling (Jun 2024): carved oxheads on the exterior, no fishing-weight groove (Windle: 2 of 333 Levantine L2.3 weights are L2.3b), ~30 km from water. Bones: cattle, sheep/goat, fallow deer; hedgehog/hare judged intrusive (Horwitz). | Card names both sides. |
| bubastite-portal | "[C] some 150 vs 156" | 156 name rings; "some 150" is not an error. Megiddo fragment came from Schumacher's spoil heap (1925/26), confirmed. | No change. |
| black-obelisk | Jehu vs envoy | Open reading; caption names Jehu as payer, figure may be king or envoy. | No change. |
| kurkh-monolith, sennacherib-prism, jehoiachin-tablets | "[C]" site/museum wording | Kurkh (Üçtepe, Diyarbakır) lay in Assyrian territory; the Taylor and Chicago prisms carry the same text; the Vorderasiatisches Museum is inside the Pergamon Museum building. | No change. Pedantry, not error. |
| ark-design Durupınar card | (August status) | Sept 2026 field report: control holes outside; organic-rich intervals; water-retaining cavity; bit broke at 4-5 m; GOPHER robot to ~12 m; no bedrock/limestone in interior holes; carbon +40% inside. Atila: "100% proven" headlines misleading, and the data "astonishes"; carbon results in 2-3 months. 1988 cores met bedrock at 5 m in two holes: the lab must resolve it. | Card updated to the September record, both sides. |

Everything below this line is the earlier machine audit, kept for the record. Its **[S]** (authority-word
status) and **[P]** (non-primary citation) tags are fair; its **[C]** tags are not to be trusted without the
table above.

---


Audited 2026-09-27. Read-only: no storybook file was changed.

**Inputs**
- Cards: `/home/cisco/storybook/data/artifacts.json` (key `artifacts`, 29 mapped cards)
- Ark card: `/home/cisco/storybook/data/chapters/ark-design.json` at `science.evidence[5]`
- Records: `scratchpad/arch/out/<id>.json`

**Tags**
- **[C]** The record contradicts the card.
- **[U]** The record shows the claim is unsupported, overstated or outdated, or that the card presents a reading as a finding.
- **[S]** The status is an authority word ("Accepted", "Firmly accepted", "standard reading") rather than evidence.
- **[P]** The citation is not the primary or first publication, and the record has one.

**How the replacement text is written.** Every suggested sentence below uses only what the record says. Where the record could not check something (for example Weidner 1939, Redford's pages, or the university's 28 Aug 2026 release), that is stated.

---

## tall-el-hammam  (record: tall-el-hammam)
No change needed. The date, site, retraction and citation all match the record: 1661 ± 21 BCE, rounded to c. 1650; Sci. Rep. 15:14291, 24 Apr 2025; 11 authors disagreeing. The status already gives evidence.
- Optional: the record gives the destruction debris as "up to c. 1.5 m thick" (Bunch et al. 2021, https://www.nature.com/articles/s41598-021-97778-3). The detail field could carry that figure.

---

## merneptah-stele  (record: merneptah-stele)
- **[U]** date "c. 1209 BCE" → the record gives "Year 5 of Merneptah, 3rd month of Shemu, day 3 (c. 1208 BCE on the conventional Egyptian chronology)". The stone gives only the regnal year. Source: Breasted, ARE III §607, https://archive.org/details/ancientrecordsof03brea
  - Replacement **date**: "Year 5 of Merneptah (c. 1208 BCE on the conventional chronology; the stone gives only the regnal year)"
- **[U]** detail "…matching a tribal confederation in the Judges period" → the record says the stone proves only that Egyptian scribes classed Israel as a people, not a city-state. Hasel (BASOR 296, 1994) argues for a sedentary/agricultural group, and the stela "says nothing about how or when Israel arrived". Source: Hasel, https://www.journals.uchicago.edu/doi/10.2307/1357179
  - Replacement **detail**: "'Israel is desolated, his seed is not' (Breasted's translation). Ashkelon, Gezer and Yenoam carry the city/foreign-land sign; Israel alone carries the sign for a people. Our reading: that fits a people without a single city-state. The stone does not say what kind of group it was, or when it arrived."
- **[S]** status "Firmly accepted."
  - Replacement **status**: "Found by Petrie in 1896 in Merneptah's mortuary temple at western Thebes. It is a reused Amenhotep III stela, with Merneptah's 28-line text on the back. Line 27 spells y-s-r-i-a-r with the people-classifier. A fragmentary duplicate stood at Karnak."
- **[P]** citation "Merneptah (Israel) Stele, Cairo Museum." (with a Wikipedia URL) → the record has the excavation report and a translation.
  - Replacement **citation**: "Egyptian Museum, Cairo JE 31408. W. M. F. Petrie, Six Temples at Thebes (1897) §24 (text first edited by W. Spiegelberg). Translation: J. H. Breasted, Ancient Records of Egypt III (1906) §§602-617." URL: https://archive.org/details/sixtemplesattheb00petruoft

## soleb-yhw  (record: soleb-inscription)
- **[C]** status "The hieroglyphic reading is not disputed." → the record says the last sign is disputed. The excavation report (Soleb III pp. 122-123) printed the quail-chick w (G43). Kennedy's 2019 collation from new photographs reads the vulture/aleph (G1). Adrom & Müller (2017) follow the older reading. Source: Kennedy, Dotawo 6 (2019) 175-192, https://escholarship.org/uc/item/07x6659z
- **[U]** status "The identification of yhwꜣ with the God of Israel is the standard reading…" → "standard reading" is a consensus label. The record gives the evidence on both sides. Kennedy (2019) says yes, because the name is not a known place-name, has no land classifier and sits beside names he reads as divine. Adrom & Müller (BZAW 484, 2017) hold that the sequence cannot be shown to be a tribe, a place or a deity. Source: https://www.degruyterbrill.com/document/doi/10.1515/9783110448221-005/html
- **[U]** date "…the list reflects the late 15th c. BCE" → the record says the column gives only the king. Kennedy puts the lists at 1409-1385 BCE on a high chronology; on lower chronologies Amenhotep III's jubilee falls in the 1360s.
  - Replacement **date**: "Reign of Amenhotep III, carved by his Year-30 jubilee (c. 1409-1385 BCE on Kennedy's high chronology; the 1360s on lower ones)"
  - Replacement **status**: "The sign sequence is y-h-w plus a final bird. The excavators read that bird as w; Kennedy's 2019 collation reads aleph. The name has no land classifier and no god-sign. Kennedy reads it as the divine name YHWH. Adrom & Müller (2017) hold that it cannot be shown to be a tribe, a place or a god. Redford (1992) places these Shasu in or near Edom. The column itself gives no geography beyond 'Shasu'."
  - Note: the record confirms only Redford's Edom placement, via Kennedy nn. 33 and 49. The card's "Yahweh was first worshipped as an Edomite god" was not checked by the record.
- **[S]** "standard reading" / "Redford calls it undoubted": authority language (see replacement status above).
- **[P]** citation relies on Redford 1992 → the record has the excavation publication and a first-hand collation.
  - Replacement **citation**: "Column IV N4 (a2), hypostyle hall, temple of Amun, Soleb (in situ). Also wall block SB 69, and a later copy at Amara West. Schiff Giorgini, Robichon, Leclant, ed. Beaux, Soleb V (IFAO 1998). T. Kennedy, Dotawo 6 (2019) 175-192. F. Adrom & M. Müller, in The Origins of Yahwism (2017) 93-114." URL: https://escholarship.org/uc/item/07x6659z

## jericho-cityiv  (record: jericho)
- **[U]** date "c. 1550–1400 BCE (disputed)" → the record names two separate dates, and the newest evidence supports the earlier one. First, 1550-1525 BCE: new 14C from the Italian-Palestinian excavation (Nigro & Yasine, VO 29, 2024). Short-lived grain from Kenyon's destruction layer (3306 ± 7 BP, Bruins & van der Plicht 1995) also calibrates to the late 17th or 16th century. Second, c. 1400 BCE: Garstang 1935, and Wood 1990, which rests on pottery, scarabs and one charcoal date (BM-1790, 1410 ± 40). ABR's repost of Wood now flags an update on that datum. Source: https://www.vicino-oriente-journal.it/index.php/vicinooriente/article/view/458
  - Replacement **date**: "End of the last Middle Bronze city (Garstang's City IV): 1550-1525 BCE by radiocarbon (Nigro & Yasine 2024; Bruins & van der Plicht 1995), or c. 1400 BCE by Wood's 1990 reading of pottery and scarabs"
- **[U]** status "Dating debated (Kenyon vs. high-chronology)." → this is outdated. The c. 1400 case is Wood's pottery-and-scarab argument, not a "high chronology". The radiocarbon published since 1995, and again in 2024, sides with Kenyon's date. The 2024 report also documents 15th-century Late Bronze reoccupation.
  - Replacement **status**: "Radiocarbon on short-lived grain (1995) and new 14C samples (2024) date the final Middle Bronze destruction to the 16th century BCE. Wood (BAR 16:2, 1990) argued for c. 1400 from local pottery, a scarab series and one charcoal date; Bienkowski (BAR 16:5) replied. The 2024 report also documents 15th-century Late Bronze rooms over the burned city."
- **[U]** detail "Revetment walls collapsed outward forming a ramp… (short siege, city 'devoted' to destruction)" → the record says mudbrick "collapsed against the stone revetment". It lists the cause of the collapse as unknown: "the excavation reports describe the collapse but do not settle its cause". "Short siege" and "devoted" are readings from Joshua, not findings.
  - Replacement **detail**: "The city was burned. Mudbrick collapsed against the stone revetment at the base of the rampart. Houses were left with jars full of grain (Kenyon recovered 'six bushels of grain in one season', per Wood). Our reading: unplundered grain fits a short siege and a city not looted. The reports do not settle what brought the walls down."
- **[P]** citation "Kenyon & later excavations, Tell es-Sultan" → the record has the primary reports.
  - Replacement **citation**: "J. Garstang, PEQ 67 (1935) 61-68. K. M. Kenyon, Digging Up Jericho (1957). H. J. Bruins & J. van der Plicht, Radiocarbon 37 (1995) 213-220. L. Nigro & J. Yasine, Vicino Oriente 29 (2024) 47-96. B. G. Wood, BAR 16:2 (1990). cf. Joshua 6:20." URL: https://www.vicino-oriente-journal.it/index.php/vicinooriente/article/view/458

## hazor-destruction  (record: hazor)
- **[U]** detail "fire intense enough to melt clay" → the record describes a fire "so intense that it cracked the basalt architectural elements", with ash up to about three feet. It reports no melted clay. Source: Ebeling 2003, https://bibleinterp.arizona.edu/articles/Hazor_Ebeling
- **[U]** detail "statues… decapitated/defaced — pointing to iconoclastic (Israelite) conquerors" → this is Ben-Tor's argument (BAR 39:4, 2013). Zuckerman (JMA 20/1, 2007) reads the same destruction as internal crisis and termination rituals. "No inscription naming a destroyer." Source: https://journal.equinoxpub.com/JMA/article/view/22950
  - Replacement **detail**: "The last Canaanite city ended in a fire that cracked basalt and left ash up to about three feet deep. It burned the ceremonial palace (Building 7050) with its contents in place. Statues of Canaanite and Egyptian rulers and gods were deliberately mutilated. Ben-Tor argues that neither Egyptians nor Canaanites would deface their own icons, and so points to the Israelites of Joshua 11. Zuckerman reads the same evidence as an internal collapse. No text names the attacker."
- **[U]** date "13th c. BCE" is correct, but the record adds that Bechar et al. (2021) keep "two different possible scenarios" open, and that Yadin put it c. 1230. Update, 2025: Shalvi & Bechar (Tel Aviv 52) found much of the northern lower city uninhabited in the Late Bronze Age. Source: https://doi.org/10.1553/aeundl31s45 and https://doi.org/10.1080/03344355.2025.2546275
  - Replacement **date**: "13th c. BCE (Yadin: c. 1230; Bechar et al. 2021 keep two radiocarbon-based scenarios open)"
- **[S]** status "Destruction accepted; attribution debated."
  - Replacement **status**: "Burning and statue mutilation were found in both the upper and lower cities. The attribution is argued from that pattern: Ben-Tor for the Israelites, Zuckerman for an internal crisis. The 2023- lower-city excavation shows part of the Late Bronze city was empty."
- **[P]** citation "Yadin & Ben-Tor excavations, Hazor." →
  - Replacement **citation**: "Y. Yadin, Hazor: The Head of All Those Kingdoms (Schweich Lectures, 1972). S. Bechar, A. Ben-Tor et al., Ägypten und Levante 31 (2021) 45-74. A. Ben-Tor, BAR 39:4 (2013) 27-36. S. Zuckerman, JMA 20/1 (2007). cf. Joshua 11:10-13." URL: https://doi.org/10.1553/aeundl31s45

## tel-dan-stele  (record: tel-dan-stele)
- **[U]** detail "An Aramean victory stele naming the king of 'the House of David' — extrabiblical proof of David's dynasty barely a century after his death" → the record says fragment A reads mlk yśrʾl, "king of Israel" (line 8), and bytdwd, "House of David" (line 9). The phrase "king of … House of David", and the royal names Joram and Ahaziah, come from restoring fragment B beside A. The editors themselves said A and B "cannot be joined in an obvious, unequivocal way". Langlois (IEJ 74/2, 2024), using RTI imaging and letter forms, argues that placement "must be abandoned". bytdwd names a kingdom or dynasty, not David as an individual. "Barely a century after his death" rests on biblical chronology. Source: https://michaellanglois.org/medias/langlois-2024-tel-dan-inscription-iej-74-2.pdf
  - Replacement **detail**: "An Old Aramaic victory stele in basalt. Its largest fragment reads 'king of Israel' (line 8) and bytdwd, 'House of David' (line 9). That is a 9th-century Aramaean scribe using David's name for Judah or its dynasty. The royal names on the smaller fragments ('…rm son of', '…yhw son of') were restored as Joram and Ahaziah. That depends on where those pieces sit, which Langlois (2024) argues against. The author is not named."
- **[S]** status "Firmly accepted."
  - Replacement **status**: "bytdwd on fragment A is legible and not in dispute. The placement of fragments B1+B2, and so the restored names Joram and Ahaziah, is contested (Langlois, IEJ 2024: different letter strokes and line spacing; no physical join between A and B1). Elgvin (2022) raised forgery; Langlois answers that the difference in hand is not evidence of forgery."
- **[P]** citation "Tel Dan Stele; Biran & Naveh." →
  - Replacement **citation**: "Israel Museum, IAA 1993-3162, 1996-125. A. Biran & J. Naveh, IEJ 43 (1993) 81-98 and IEJ 45 (1995) 1-18. M. Langlois, IEJ 74/2 (2024) 59-79." URL: https://www.imj.org.il/en/collections/371407

## khirbet-qeiyafa  (records: khirbet-qeiyafa-ostracon + khirbet-qeiyafa-fortifications)
- **[U]** detail "a proto-Canaanite ostracon with melech (king), shofet (judge), eved (servant)" → the record says those are contested readings. Millard (Tyndale Bulletin 62.1, 2011), following Cook, reads a list of personal names: Ellat-ʿash, ʿEbed-…, Shaphat, Bodmilk. On that reading špṭ is the name Shaphat and mlk sits inside the name bdmlk. The language is disputed (Hebrew, Canaanite, Phoenician or Moabite). Source: https://www.tyndalebulletin.org/article/29303-the-ostracon-from-the-days-of-david-found-at-khirbet-qeiyafa/attachment/76268.pdf
- **[U]** detail "Carbon-dated olive pits fix the city to David's era" and confirms "A fortified Judahite state" → the record gives the excavators' olive-pit 14C as c. 1000 BCE (Garfinkel et al., Radiocarbon 57, 2015). Finkelstein & Piasetzky's regional Bayesian model (Radiocarbon 57, 2015) puts it later, in the 10th century. Na'aman (JHS 17, 2017) argues nothing in the finds ties the site to Jerusalem. "David's era" is a reading of the date. Source: https://doi.org/10.5508/jhs.2017.v17.a7
- **[U]** confirms "'Shaaraim' (1 Sam 17:52)" → Garfinkel & Ganor (JHS 8, 2008) identify the site as Sha'arayim because it is the only Iron Age site in Judah or Israel with two gates. Other identifications exist, and no name is written at the site. The record adds that the gates are four-chambered.
  - Replacement **detail**: "A 2.3-hectare hilltop town above the Elah Valley. It has a casemate wall of very large stones and two four-chambered gates. The excavators identify it as Sha'arayim ('two gates'), since it is the only Iron Age site in Judah or Israel with two gates; no name is written there. Burnt olive pits from its single destruction date to c. 1000 BCE. A five-line ink ostracon is read as a text about judging and serving (Misgav, Galil, Puech), or as a list of names (Cook, Millard)."
- **[U]** status "Davidic identification debated (Finkelstein's low chronology)." → this is incomplete. It should name all three disputes.
  - Replacement **status**: "Date: c. 1000 BCE on the site's own olive pits (Garfinkel 2015), or later 10th century on a regional model (Finkelstein & Piasetzky 2015). Judahite attribution: challenged by Na'aman (2017). Ostracon: its language and meaning are disputed."
- **[P]** citation "Garfinkel excavations, Khirbet Qeiyafa." (URL: armstronginstitute.org) →
  - Replacement **citation**: "Y. Garfinkel & S. Ganor, Khirbet Qeiyafa Vol. 1 (IES/Hebrew University 2009), including H. Misgav et al., 'The Ostracon', pp. 243-257. Garfinkel & Ganor, JHS 8 (2008) art. 22. Garfinkel et al., Radiocarbon 57.5 (2015) 881-890. A. Millard, Tyndale Bulletin 62.1 (2011)." URL: https://doi.org/10.5508/jhs.2008.v8.a22

## mesha-stele  (record: mesha-stele)
- **[C]** detail "(reconstructed, confirmed by 2023 imaging) the 'House of David'" and status "'House of David' line confirmed by recent imaging" → the record contains no 2023 imaging, and nothing it cites says "confirmed". What it does have: Langlois (Semitica 61, 2019, RTI of the stone and the 1868 squeeze) calls bt[d]wd "hypothetical but … the most probable reading". Lemaire & Delorme (BAR 48, Nov 2022) say new photographs "clearly establish the presence of the first dalet and confirm the last dalet, while only the letter taw remains somewhat unclear". Finkelstein, Na'aman & Römer (Tel Aviv 46, 2019) read a three-consonant name beginning with b and propose Balak. Source: https://doi.org/10.1080/03344355.2019.1586378
  - Replacement **detail**: "A basalt stele, 125 cm high, with 34 lines in Moabite. It names Omri king of Israel and his son. It names Yahweh, whose altar-hearths or vessels Mesha took from Nebo. Line 31 is damaged. Lemaire reads 'House of David' there; the RTI and photographic studies of 2019 and 2022 support the dalets. Finkelstein, Na'aman and Römer read the name Balak instead."
- **[S]** status "Accepted; …"
  - Replacement **status**: "The text is secure, from Clermont-Ganneau's 1868 squeeze and the reassembled stone. The Line 31 reading is argued from new imaging on both sides: Langlois 2019 and Lemaire & Delorme 2022 for bt[d]wd; Finkelstein, Na'aman & Römer 2019 for Balak."
- **[P]** citation "Mesha Stele, Louvre; Lemaire reading." →
  - Replacement **citation**: "Louvre AO 5066. C. Clermont-Ganneau, La stèle de Dhiban (Paris 1870). M. Langlois, Semitica 61 (2019) 23-47. I. Finkelstein, N. Na'aman & T. Römer, Tel Aviv 46.1 (2019) 3-11. A. Lemaire & J.-P. Delorme, BAR 48 (Nov 2022)." URL: https://collections.louvre.fr/en/ark:/53355/cl010120339

## kurkh-monolith  (record: kurkh-monolith)
- **[C]** site "Assyria" → the record says it was found in 1861 by J. G. Taylor, British consul, at Kurkh (modern Üçtepe Höyük), Bismil district, Diyarbakır province, south-eastern Turkey, on the upper Tigris. It is now BM 118884. Source: BM record https://www.bmimages.com/preview.asp?image=00150815001 ; Taylor, JRGS 35 (1865), https://doi.org/10.2307/3698077
  - Replacement **site**: "Kurkh (Üçtepe), Diyarbakır province, SE Turkey (British Museum)"
- **[U]** detail "…'Ahab the Israelite' contributing 2,000 chariots — the largest chariot force…" → the stone as carved reads 2 LIM (2,000), and that is the largest figure in the list. However, Na'aman (Tel Aviv 3, 1976) argues it is a scribal error for 200: it is out of scale with Damascus (1,200) and Hamath (700), and the stela has other scribal errors. Yamada (2000) collated the signs. The record also notes that Assyria fought the same coalition again in years 11 and 14, so the claimed rout is open to question. Source: https://doi.org/10.1179/033443576788497930
  - Replacement **detail**: "Shalmaneser III's account of Qarqar (853 BCE) lists '2,000 chariots, 10,000 soldiers of Ahab, the Israelite', the largest chariot figure in the coalition as carved. Na'aman argues the scribe meant 200. This is the earliest dated text outside the Bible to name a king of Israel."
- **[S]** status "Accepted."
  - Replacement **status**: "The name reads a-ha-ab-bu KUR.sir-ʾa-la-a-a on the stone (RIMA 3 A.0.102.2, line ii 91-92). The chariot figure as carved is 2,000; whether it is a scribal error is argued (Na'aman 1976; Yamada 2000)."
- **[P]** citation "Kurkh Monoliths, British Museum." →
  - Replacement **citation**: "BM 118884. A. K. Grayson, RIMA 3 (1996) A.0.102.2. J. G. Taylor, JRGS 35 (1865). Translation: Luckenbill, ARAB I (1926) §611." URL: https://oracc.museum.upenn.edu/riao/Q004607

## black-obelisk  (record: black-obelisk)
- **[U]** date "c. 841 BCE" → 841 BCE is the year of Jehu's payment: the 18th regnal year, according to parallel annals (RIMA 3 A.0.102.8, 10). The obelisk's own text runs to the 31st year (828 BCE), and the monument itself dates to c. 825 BCE. Source: https://oracc.museum.upenn.edu/riao/Q004693
  - Replacement **date**: "c. 825 BCE (text runs to 828 BCE); Jehu's payment 841 BCE"
- **[U]** confirms "the only known image of an Israelite king" and detail "a panel shows the king bowing" → the record says the caption names Iaua as the payer, but "does not say he was present in person". The kneeling figure may be the king or an envoy. The Oracc Nimrud project reads it as Jehu himself. The caption says DUMU Ḫumrî ("son of Omri"), which the RIAo translation renders as the state name, Bīt-Ḫumrî.
  - Replacement **confirms**: "Jehu of Israel paying tribute to Assyria. The kneeling figure may be the king himself, which would make it the only known picture of an Israelite king, or his envoy."
  - Replacement **detail**: "'Tribute of Iaua (Jehu), son of Omri' (Luckenbill). A figure kneels at Shalmaneser's feet in the register above that caption. The caption names the payer; it does not say whether he came in person."
- **[S]** status "Accepted."
  - Replacement **status**: "The epigraph over register 2 names Iāūa 'son of Ḫumrî'. Parallel annals place the payment in 841 BCE, which fits Jehu. McCarter (1974) proposed Joram instead; Weippert (1978) kept Jehu."
- **[P]** citation "Black Obelisk, British Museum." (discerninghistory URL) →
  - Replacement **citation**: "BM 118885. A. K. Grayson, RIMA 3 (1996) A.0.102.14 and 88. Translation: Luckenbill, ARAB I (1926) §590. Found by A. H. Layard at Nimrud, 1846." URL: https://oracc.museum.upenn.edu/riao/Q004693

## lachish-siege  (record: lachish-reliefs)
- **[U]** date "701 BCE" → that is the date of the siege. The reliefs were carved for Sennacherib's South-West Palace, dated by the British Museum to c. 700-681 BCE. They also carry a cuneiform caption, which the card omits: "…the booty of Lachish passed before him" (Luckenbill §489). Source: https://www.britishmuseum.org/explore/galleries/middle_east/room_10b_assyria_siege_of_la.aspx
  - Replacement **date**: "Siege 701 BCE; reliefs carved c. 700-681 BCE"
- **[S]** status "Firmly accepted — triple-attested…"
  - Replacement **status**: "Attested three ways. The relief's caption names Sennacherib and Lachish. The annals give the 701 campaign. The Assyrian siege ramp was excavated at Tel Lachish (Ussishkin)."
  - Note: the record does not address the card's "only known Assyrian siege ramp", the counter-ramp, or the arrowheads and armour scales. It neither supports nor contradicts them.
- **[P]** citation "Lachish Reliefs, British Museum; Tel Lachish excavations." →
  - Replacement **citation**: "British Museum Room 10b (South-West Palace, Room XXXVI). A. H. Layard, Discoveries in the Ruins of Nineveh and Babylon (1853) 148-153. Epigraph: Luckenbill, ARAB II §489. D. Ussishkin, Journal for Semitics 24.2 (2017) 719-758." URL: https://doi.org/10.25159/1013-8471/3477

## sennacherib-prism  (record: taylor-prism-sennacherib)
- **[C]** citation "Sennacherib Prism, British Museum / Oriental Institute" → this merges two objects. The Taylor Prism is BM 91032, dated 691 BCE by its eponym. The Chicago prism, OIM A2793 (689 BCE), is a separate copy of the same text. Source: https://www.britishmuseum.org/collection/object/W_1855-1003-1
- **[U]** site "Nineveh" → Col. Taylor bought it in 1830. It is only "said to have been found at Nebi Yunus", and it has no excavation context (BM record).
  - Replacement **site**: "Said to be from Nebi Yunus, Nineveh (bought 1830; no excavation record). British Museum."
- **[U]** detail "…matching the biblical account of the Assyrian withdrawal" → the record says there is "no claim that Jerusalem was entered or taken, and no account of the Assyrian army's withdrawal". The prism is silent on withdrawal, so it cannot match an account of one. It gives the tribute as 30 talents of gold and 800 of silver; 2 Kgs 18:14 gives 30 of gold and 300 of silver.
  - Replacement **detail**: "'Himself, like a caged bird, I shut up in Jerusalem, his royal city' (Luckenbill §240). The prism claims 46 walled towns taken, then tribute sent after the king to Nineveh (30 talents of gold and 800 of silver; 2 Kgs 18:14 has 300 of silver). It never claims Jerusalem was taken, and says nothing of how the campaign ended. That silence is what both readings rest on."
- **[S]** status "Accepted."
  - Replacement **status**: "The eponym date, 691 BCE, is on the prism. The same third-campaign text appears on the Chicago Prism (689 BCE) and the Jerusalem Prism. No edition claims Jerusalem fell."
- **[P]** →
  - Replacement **citation**: "BM 91032 (Taylor Prism). A. K. Grayson & J. Novotny, RINAP 3/1 (2012) text 22, ii 37-iii 49. Translation: Luckenbill, ARAB II (1927) §§239-240." URL: https://epub.ub.uni-muenchen.de/119669/1/Grayson_Novotny_RINAP_3_1.pdf

## hezekiah-tunnel  (records: hezekiah-tunnel-inscription + hezekiah-broad-wall)
- **[U]** date "c. 701 BCE" → the inscription names no king and no year. The tunnel is dated c. 700 BCE by radiocarbon on plant matter in its plaster and U-Th on speleothems (Frumkin, Shimron & Rosenbaum, Nature 425, 2003). Reich & Shukron (Tel Aviv 38, 2011) argue from pottery for the early 8th century. The Siloam Dam dates of 805-795 BCE (PNAS 2025) date the dam, not the tunnel. Source: https://www.nature.com/articles/nature01875
  - Replacement **date**: "Tunnel c. 700 BCE by radiometric dating (2003); early 8th c. argued from pottery (2011). The inscription carries no date."
- **[U]** confirms "Hezekiah's water tunnel" → the text is a builders' record that names no king, date or god. The link to Hezekiah rests on the fit with 2 Kgs 20:20 and 2 Chr 32:30, and on the 2003 dates.
- **[U]** detail "A 533 m tunnel" → the record gives no 533 m figure. The inscription gives 1,200 cubits. Barton (1917), after the Parker clearance, gives "about 1,700 feet". Source: https://www.gutenberg.org/files/43070/43070-h/43070-h.htm
- **[U]** detail "plus a 7 m-thick wall housing refugees from the fallen north" → the Broad Wall is about 7 m wide, which matches. But the refugee explanation is "an inference about why the city grew, not something the wall itself shows". Regev et al. (PNAS 121/19, 2024) move Jerusalem's major 8th-century fortifications from Hezekiah to late Uzziah, though from samples in other areas, not this wall. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC11087761/
  - Replacement **detail**: "A tunnel cut through rock from the Gihon Spring to the Siloam Pool. Its six-line inscription records two crews cutting toward each other until they met 'axe against axe', and water flowing 1,200 cubits to the pool. It names no king. Also: the 'Broad Wall', about 7 m wide, built over razed houses on the Western Hill (cf. Isa 22:10). Avigad assigned it to Hezekiah. 2024 radiocarbon from other parts of Jerusalem moves the city's big 8th-century fortifications to Uzziah."
- **[S]** status "Accepted."
  - Replacement **status**: "The inscription is Iron Age Hebrew; its letter forms were defended against a Hasmonean date in 1996. The tunnel is dated c. 700 BCE by radiometric methods (Frumkin et al. 2003), and an early-8th-century date is argued from pottery (Reich & Shukron 2011). The Broad Wall's builder, Hezekiah or Uzziah, is open."
- **[P]** citation "Siloam Inscription, Istanbul Museum; Jewish Quarter excavations." →
  - Replacement **citation**: "Istanbul Archaeology Museums. A. H. Sayce, PEFQS 13 (1881) 69-73 and 141-157. A. Frumkin et al., Nature 425 (2003) 169-171. Broad Wall: H. Geva (ed.), Jewish Quarter Excavations I (2000); N. Avigad, Discovering Jerusalem (1983)." URL: https://www.tandfonline.com/doi/abs/10.1179/peq.1881.13.2.69

## hezekiah-bulla  (record: hezekiah-bulla)
- **[C]** detail "Found 2015 in controlled excavation." → the bulla was excavated in the 2009 season, from an Iron Age refuse dump in Ophel Area A. It was identified during wet-sifting and announced on 2 Dec 2015. Source: Hebrew University release, https://www.sciencedaily.com/releases/2015/12/151202132519.htm
  - Replacement **detail**: "A clay bulla, 13 × 12 mm: 'Belonging to Hezekiah [son of] Ahaz, king of Judah'. The word 'son' is not written. It shows a two-winged sun with downturned wings between two ankhs. It came from 2009-season soil of a refuse dump beside the Ophel 'Royal Building', was found in wet-sifting, and was announced in 2015. It is the first seal impression of a Judahite or Israelite king recovered in a controlled excavation."
- **[S]** status "Accepted."
  - Replacement **status**: "The legend is legible and names Hezekiah, Ahaz and the title 'king of Judah'. The excavators date the dump to Hezekiah's time or shortly after."
- **[P]** citation "Mazar, Ophel excavations (2015)." (BAS list URL) →
  - Replacement **citation**: "E. Mazar (ed.), The Ophel Excavations to the South of the Temple Mount 2009-2013, Final Reports Vol. I (2015), ch. 13, pp. 628-639. Hebrew University release, 2 Dec 2015." URL: https://www.sciencedaily.com/releases/2015/12/151202132519.htm

## ketef-hinnom  (record: silver-amulets-ketef-hinnom)
- **[U]** confirms "…earliest biblical text known" and detail "…attesting the pre-exilic existence of Torah liturgy" → the record describes them as "the oldest known objects carrying wording also found in the Hebrew Bible" (on the late pre-exilic dating). It says they are "amulets, not biblical manuscripts". KH2 leaves out a clause of Num 6:25b-26a and adds non-biblical formulas ("rebuker of Evil"). KH1 carries the Deut 7:9 formula. "The objects show the wording existed; they do not show which written book, if any, it came from." Source: Barkay et al., BASOR 334 (2004), https://doi.org/10.2307/4150106
  - Replacement **confirms**: "Wording of the Priestly Blessing (Num 6:24-26) in use before the Exile. These are the oldest known objects carrying words also found in the Bible."
  - Replacement **detail**: "Two rolled silver amulets from a tomb repository, found in 1979. KH2 reads 'May YHWH bless you, keep you; may YHWH make his face shine upon you and grant you peace'. That is a shorter form of Num 6:24-26, alongside other protective formulas. KH1 adds 'the covenant and loving-kindness toward those who love him and keep his commandments' (Deut 7:9)."
- **[U]** date "c. 600 BCE" with status "Accepted." → Barkay et al. (2004) place them late pre-exilic, from palaeography and the surrounding pottery. Waaler (Tyndale Bulletin 53, 2002) argues 725-650 BCE. Renz & Röllig (1995) reportedly left a later date open; the record flags that report as unchecked.
- **[S]** status "Accepted."
  - Replacement **status**: "Dated by letter forms and the tomb deposit: late pre-exilic, c. 600 BCE (Barkay et al. 2004), or 725-650 BCE (Waaler 2002). No date is written on them."
- **[P]** citation "Barkay, Ketef Hinnom (1979)." → 1979 is the year of excavation, not a publication.
  - Replacement **citation**: "Israel Museum, IAA 1980-1495, 1980-1496. G. Barkay, Tel Aviv 19/2 (1992) 139-192. G. Barkay, M. J. Lundberg, A. G. Vaughn & B. Zuckerman, BASOR 334 (2004) 41-71." URL: https://doi.org/10.2307/4150106

## lachish-letters  (record: lachish-letters)
- **[U]** detail "…'for we cannot see Azekah' — capturing the moment Azekah fell" → the record says "The letter itself only says the post could not see Azekah… The text does not say Azekah fell." The link to Jer 34:7 is a reading. Source: Torczyner 1938, https://archive.org/details/lachishletters0000harr
  - Replacement **detail**: "Military letters on potsherds from Hoshayahu to his superior Ya'ush. Letter 4 closes: they are watching for the signal-fires of Lachish, 'for we cannot see Azekah'. Our reading, with Jer 34:7: Azekah had gone dark, leaving Lachish among the last cities standing. The letter itself says only that Azekah could not be seen."
- **[U]** citation "British Museum / Israel Museum" → the record says most are in the British Museum. A smaller group, including Letter 6, is in Jerusalem, at the Rockefeller Museum / IAA. It found no Israel Museum holding.
- **[S]** status "Accepted."
  - Replacement **status**: "Twenty-one ink ostraca, found in the burnt gate complex of Level II. Where they were written is disputed: letters from an outpost (Torczyner, Rainey) or drafts kept at Lachish (Yadin)."
- **[P]** →
  - Replacement **citation**: "British Museum; Rockefeller Museum/IAA (Letter 6 and others). H. Torczyner, Lachish I: The Lachish Letters (1938). A. F. Rainey, PEQ 119 (1987) 149-151." URL: https://archive.org/details/lachishletters0000harr
- Minor: the date "c. 589 BCE" could read "c. 588-586 BCE (destruction layer)".

## jehoiachin-tablets  (record: jehoiachin-rations-tablets)
- **[U]** confirms "…2 Kings 25:27–30" and detail "…confirming the exiled king's treatment in captivity" → the only dated Jehoiachin tablet is from year 13 of Nebuchadnezzar (592/591 BCE). That is about 30 years before the release in 2 Kgs 25:27 (c. 561). The record says the tablets "match 2 Kgs 24:15 (deportation to Babylon) and the kind of allowance in 25:30, not the release event itself", and "say nothing about prison". Source: https://doi.org/10.13173/9783447124140 ; CoJS summary.
  - Replacement **confirms**: "King Jehoiachin of Judah and his sons held at Babylon on royal rations (2 Kings 24:15; cf. 25:30)"
  - Replacement **detail**: "Palace ration lists issue oil to 'Ya'ukin, king of the land of Yahudu', to 'the five sons of the king of Yahudu', and to other Judahites. One tablet is dated 592/591 BCE, three decades before the release told in 2 Kings 25:27. Pedersén's 2025 full edition notes that Jehoiachin's was the largest single oil allocation in the archive."
- **[C]** citation "Babylon ration tablets, Pergamon Museum." → they belong to the Vorderasiatisches Museum, Berlin, which is housed in the Pergamonmuseum building. Its galleries have been closed since 23 Oct 2023, with reopening expected in 2037. Source: https://www.smb.museum/en/museums-institutions/pergamonmuseum/refurbishment/
- **[S]** status "Accepted."
  - Replacement **status**: "Excavated by Koldewey in 1902-03 from the Vaulted Building of the Southern Palace. The Jehoiachin entries were identified by E. F. Weidner (published 1939), and the full archive of 527 texts was published by O. Pedersén (2025)."
- **[P]** →
  - Replacement **citation**: "Vorderasiatisches Museum, Berlin. E. F. Weidner, 'Jojachin, König von Juda…', Mélanges Dussaud II (1939); the record could not open it. O. Pedersén, The South Palace Archives in Babylon (2025). R. Koldewey, The Excavations at Babylon (1914) 91-100." URL: https://doi.org/10.13173/9783447124140

## cyrus-cylinder  (record: cyrus-cylinder)
- **[U]** confirms "Cyrus's policy of repatriation behind the return from exile" and detail "Records Cyrus allowing deported peoples to return and rebuild their temples" → lines 30-32 return the gods and gather the inhabitants of a named list of Mesopotamian and trans-Tigris cities only. The cylinder does not mention Judah, Jerusalem, the Jews or YHWH. Kuhrt (JSOT 25, 1983) argues it is a Babylonian building inscription and not evidence of an empire-wide policy. Any link to Ezra 1 is an inference from the parallel. Source: https://doi.org/10.1177/030908928300802507 ; Rogers 1912 p. 383.
  - Replacement **detail**: "A clay foundation cylinder for Babylon's wall. In it Cyrus says that, at Marduk's command, he returned the gods of Ashur, Susa, Der and other cities east of the Tigris to their shrines, 'and all their inhabitants I collected and restored to their dwelling places'. It names no western city and no Jews. The link to Ezra 1 is that the act is the same kind of act."
- **[U]** date "539 BCE" → the British Museum gives "539 BC (after)". No regnal year is preserved.
  - Replacement **date**: "After Cyrus took Babylon in 539 BCE"
- **[S]** status "Accepted."
  - Replacement **status**: "The text is intact apart from gaps. Yale fragment NBC 2504 restores lines 36-45, and two tablet copies were identified in 2009-10. How far it reflects an empire-wide policy is argued (Kuhrt 1983)."
- **[P]** citation "Cyrus Cylinder, British Museum." →
  - Replacement **citation**: "BM 90920 (excavated by H. Rassam, Babylon, 1879). Translation: R. W. Rogers, Cuneiform Parallels to the Old Testament (1912) 380-384. A. Kuhrt, JSOT 25 (1983) 83-97." URL: https://www.britishmuseum.org/collection/object/W_1880-0617-1941

## pilate-stone  (record: pilate-inscription)
- **[U]** detail "A dedication naming 'Pontius Pilatus, Prefect of Judea' — confirming … his exact Roman title (Praefectus)" → the record says no verb survives; line 4 shows only an apexed E. "Dedicated", "made" and "rebuilt" are all restorations. Alföldy (SCI 18, 1999) reads a secular harbour tower rebuilt, not a dedication. The title reads [PRAEF]ECTUS IUDA[EA]E: -ECTUS survives and "PRAEF" is restored. The block was found reused as a theatre step. Source: Taylor, NTS 52 (2006), https://researchcommons.waikato.ac.nz/server/api/core/bitstreams/194607b9-dabd-4053-962a-afe8b010466f/content
  - Replacement **detail**: "A limestone block with four broken Latin lines: '[…]S TIBERIEUM / [PO]NTIUS PILATUS / [PRAEF]ECTUS IUDA[EA]E'. It names Pilate with the title prefect, not procurator, and a building called a Tiberieum. The verb and the purpose are lost; editors restore either a cult building or a harbour tower."
- **[S]** status "Accepted."
  - Replacement **status**: "The name and title are on the stone. It is the only object that names Pilate with his office. Philo and Josephus write about him."
- **[P]** citation "Pilate Stone (1961), Israel Museum." →
  - Replacement **citation**: "Israel Museum, IAA 1961-529. A. Frova, Rendiconti dell'Istituto Lombardo 95 (1961) 419-434. G. Alföldy, SCI 18 (1999) 85-108. J. E. Taylor, NTS 52 (2006) 555-582." URL: https://www.imj.org.il/en/collections/395572

## caiaphas-ossuary  (record: caiaphas-ossuary)
- **[U]** detail "…containing the bones of a ~60-year-old man — matching Josephus's 'Joseph who was called Caiaphas'" → the box held the bones of six people: two infants, a child of 2-5, a youth, an adult woman and a man of about 60. Neither Caiaphas ossuary carries a title such as priest or high priest. Greenhut framed the identification as "another question", not a finding. The name is spelled two ways on the box (Qayafa' / Qafa'). The bones were reburied on the Mount of Olives. Source: Greenhut, BAR 18:5 (1992), https://library.biblicalarchaeology.org/article/burial-cave-of-the-caiaphas-family/
  - Replacement **detail**: "The most ornate ossuary in a family tomb found in 1990 is inscribed 'Yehosef bar Qayafa'' and 'Yehosef bar Qafa'', meaning Joseph son of Caiaphas. Josephus calls the high priest 'Joseph who was called Caiaphas'. The box held six people, among them a man of about 60. No priestly title is written on it. That he is the high priest is a reading the excavator himself posed as a question."
- **[S]** status "Accepted."
  - Replacement **status**: "The inscriptions are clear and the tomb is Second Temple (an Agrippa I coin of 42/43 CE was found in another box). The identity of the 60-year-old man is not written."
- **[P]** citation "Caiaphas Ossuary (1990), Israel Museum." →
  - Replacement **citation**: "Israel Museum (IAA). Z. Greenhut, 'The "Caiaphas" Tomb in North Talpiyot', 'Atiqot 21 (1992), with R. Reich, 'Ossuary Inscriptions from the Caiaphas Tomb'. Z. Greenhut, BAR 18:5 (1992). W. Horbury, PEQ 126 (1994) 32-48." URL: https://library.biblicalarchaeology.org/article/burial-cave-of-the-caiaphas-family/

## pool-of-bethesda  (record: bethesda-pool)
- **[C]** detail "Excavation revealed a rectangular pool split by a central dyke — two basins, four surrounding colonnades plus a fifth on the dyke: exactly five porticoes" → the record says "No standing colonnades were found; the five porticoes are a reconstruction argued from John 5:2 and the twin-pool plan." In 1888 the PEF editors reasoned from the verse to the plan: "the only possible way for a pool to have five porticoes… is to be a double or twin pool". Source: Schick, PEF QS July 1888, https://archive.org/details/palestine-exploration-quarterly_1888-07
  - Replacement **detail**: "Excavation at St. Anne's found two rock-cut basins separated by a dividing wall. One basin was 55 ft by 12.5 ft, cut 30 ft deep, with 24 steps. John's 'five porticoes' fit this plan as colonnades on the four sides and one on the dividing wall. That is a reconstruction; no standing colonnades were found. Von Wahlde (2011) reads the stepped southern basin as a ritual bath."
- **[U]** date "1st c. CE" → the record says the pools are rock-cut and "in use in the Second Temple period". Their construction dates were not established from an excavation report, and a flat "1st century CE" is unsourced.
  - Replacement **date**: "Rock-cut pools in use in the Second Temple period (construction date not fixed)"
- **[S]** status "Accepted."
  - Replacement **status**: "The twin pool is physically there. The porticoes are inferred from John 5:2 and the plan. Pilgrim testimony ties the site to the name from the 4th century on."
- **[P]** citation "Bethesda excavations, Jerusalem." →
  - Replacement **citation**: "C. Schick, PEF Quarterly Statement 20:3 (1888) 115-134 and 22:1 (1890) 18-20. U. C. von Wahlde, BAR (Sept/Oct 2011)." URL: https://archive.org/details/palestine-exploration-quarterly_1888-07

## gallio-inscription  (record: gallio-inscription)
- **[U]** detail "…allowing Paul's stay in Corinth to be dated precisely to 51–52 CE" → the record says the letter is dated by Claudius' 26th acclamation to between late 51/early 52 and 1 Aug 52. That puts Gallio's term in 51/52 or 52/53: "the inscription alone does not decide". If Plassart's reading holds, the letter went to Gallio's successor, and the term moves. "Of Achaia" and part of "proconsul" are restored. Paul's dates come from combining the inscription with Acts 18 and the one-year-term rule. Source: Plassart, FD III.4 no. 286, https://epigraphy.packhum.org/text/240470 ; Oliver, Hesperia 40 (1971)
  - Replacement **detail**: "A letter of Claudius to Delphi naming 'Junius Gallio, my friend and proconsul'. It is dated by Claudius' 26th acclamation to early 52 CE (before 1 August 52). Achaia's proconsuls normally served one year, so Gallio held office in 51/52 or 52/53. This is the one fixed external point for Paul's time in Corinth (Acts 18:12)."
  - Replacement **date**: "Letter early 52 CE (before 1 Aug 52); Gallio's term 51/52 or 52/53"
- **[S]** status "Accepted."
  - Replacement **status**: "The numeral 26 is legible. Gallio's name survives; 'Achaia' is restored. Who received the letter is argued: Plassart 1970 says Gallio's successor, Oliver 1971 says Delphi."
- **[P]** citation "Gallio (Delphi) Inscription." →
  - Replacement **citation**: "Delphi Museum. É. Bourguet (1905). A. Plassart, Fouilles de Delphes III.4 (1970) no. 286. J. H. Oliver, Hesperia 40 (1971) 239-240. A. Deissmann, St. Paul (1912) App. I." URL: https://epigraphy.packhum.org/text/240470

## nuzi-tablets  (record: nuzi-tablets)
- **[U]** detail "household gods (teraphim) functioning as title-deeds — explaining why Rachel stole them (Genesis 31)" → the record says this proposal "was re-examined by M. Greenberg (JBL 81, 1962) and by M. A. Morrison (BA 46, 1983)". It did not state their conclusions. Thompson (1974) "re-examined each proposed parallel and argued that several rest on misreadings of the tablets or occur in other periods". The card states the proposal as fact. Source: https://doi.org/10.2307/3264421 ; https://doi.org/10.1515/9783110841442-011
- **[U]** detail "a childless couple adopting a servant as heir, displaced if a son is later born" → the verified text, HSS V 67, has an adopted heir (Shennima) who drops to second heir if a natural son is born. The record does not show that the adoptee was a servant. The surrogate clause is verified: if Gilimninu is childless she must give her husband a Lullu woman, and that woman's children may not be expelled.
  - Replacement **detail**: "Thousands of family-law tablets from a Hurrian town. One adoption contract (HSS V 67) says that if the wife Gilimninu bears no child, she must give her husband a Lullu woman, whose children may not be sent away (cf. Sarah and Hagar, Gen 16). If a natural son is born later, he becomes firstborn over the adopted heir (cf. Gen 15:2-4). The proposal that household gods served as title to an inheritance (cf. Rachel, Gen 31) has been re-examined (Greenberg 1962; Morrison 1983)."
  - Note: the card's Kitchen slave-price claim is not addressed by the record either way.
- **[S]** status "Tablets accepted; …"
  - Replacement **status**: "The clauses are on the tablets (Speiser 1930). Whether they date the patriarchs is argued: the 1920s-50s school (Gadd, Speiser) against Thompson (1974), who re-read each parallel."
- **[P]** citation "Nuzi archives; K. A. Kitchen, On the Reliability of the Old Testament (2003), ch. 7." → Kitchen is a secondary synthesis.
  - Replacement **citation**: "E. Chiera, Excavations at Nuzi I (HSS 5, 1929). E. A. Speiser, AASOR 10 (1930) 1-73 (HSS V 67 = text 2). T. L. Thompson, BZAW 133 (1974) ch. 10. K. A. Kitchen (2003) ch. 7 for the slave-price series." URL: https://archive.org/details/in.gov.ignca.4563

## six-chambered-gates  (records: gezer-six-chambered-gate + hazor-solomonic-gate + megiddo-stables)
- **[U]** detail "Yadin famously predicted the Gezer gate's dimensions from Hazor's before it was fully dug." → the record says Macalister had already exposed half of the gate in 1902-09 and published it as a "Maccabaean castle". In 1958 Yadin identified it as an Iron Age gate by reading Macalister's plan (IEJ 8), and Dever's team cleared it in 1967-71. The record says a claim of identical dimensions "is not supported by any source checked". Source: Yadin, IEJ 8 (1958), https://www.jstor.org/stable/i27924726 ; Macalister 1912, https://archive.org/details/excavationofgeze0001rast
- **[U]** detail "…the same architectural signature… built to one plan — as if one royal engineer corps…" → the verified wording is "almost identical in plan" (Dever 2021, reporting Yadin). "A measured side-by-side comparison was not located."
  - Replacement **detail**: "1 Kings 9:15 names the cities Solomon fortified: 'Hazor and Megiddo and Gezer'. Each has a gate with three chambers on each side of the passage. In 1958 Yadin recognised the Gezer gate in Macalister's old plan, where it had been labelled a 'Maccabaean castle', as almost identical in plan to those at Hazor and Megiddo. Dever's team then excavated it."
- **[U]** status "…10th-century (Solomon) or 9th-century (Omrides)… (Yadin/Dever vs. Finkelstein)." → this is outdated: it omits the 2023-24 radiocarbon. Webster et al. (PLOS ONE 2023) model the construction of Gezer Stratum 8 at 998-957 BCE (68.3%), from the adjacent administrative building, not the gate. Finkelstein & Piasetzky ("The Gezer Discrepancy", JEMAHS 12.4, 2024) contest it. Finkelstein et al. (Tel Aviv 46, 2019) put Megiddo's six-chambered Gate 2156 in the Omride 9th century. Hazor Stratum X has no radiocarbon date. Source: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0293119 ; https://doi.org/10.5325/jeasmedarcherstu.12.4.0411
  - Replacement **status**: "The three gates share a six-chamber plan. Their dates are argued. At Gezer, radiocarbon from the building beside the gate gives 998-957 BCE (Webster et al. 2023), challenged by Finkelstein & Piasetzky (2024). Finkelstein dates the Megiddo gate to the 9th-century Omrides. Hazor's Stratum X is argued between 10th-century (Ben-Tor) and 9th-century (Finkelstein) dates on pottery."
- **[S]** status "The gates and their shared plan are accepted" (see replacement above).
- **[P]** citation "Yadin, Hazor excavations; Dever, Gezer; cf. 1 Kings 9:15." (Wikipedia URL) →
  - Replacement **citation**: "Y. Yadin, IEJ 8 (1958) 80-86. R. A. S. Macalister, The Excavation of Gezer I (1912). Y. Yadin et al., Hazor III-IV (1989). W. G. Dever, JJAR 1 (2021) 102-125. L. C. Webster et al., PLOS ONE 18.11 (2023). I. Finkelstein et al., Tel Aviv 46.2 (2019). cf. 1 Kings 9:15." URL: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0293119
- The card does not mention the Megiddo stables, so there is nothing to check against that record.

## mt-ebal-altar  (record: mount-ebal-altar)
- **[C]** detail "…filled with bones of only kosher animals (no pig)" → the faunal breakdown is 65% caprine, 21% bovine, 10% fallow deer and 4% other, including snake and tortoise, so 96% kosher. Source: Stripling et al., Heritage Science 11 (2023), summarising Horwitz, https://www.nature.com/articles/s40494-023-00920-9
- **[C]** status "…(Stripling/Galil vs. Rollston/Mazar)" → the record says the IEJ 73/2 (2023) critical response is by Maeir & Rollston. Mazar wrote a separate article identifying the object as a fishing-net sinker, and Yahalom-Mack wrote on the lead source (Lavrion, Greece). Haughwout (Heritage Science 12:70, 2024) found "insufficient epigraphic evidence to conclude that writing exists". Source: https://www.nature.com/articles/s40494-023-01130-z
- **[C]** citation "Associates for Biblical Research (2022)" → the object was recovered in Dec 2019, announced at a press event in March 2022, and published on 12 May 2023 in Heritage Science 11:105.
- **[U]** detail omits the find context: the lead object came from Zertal's spoil heap during wet-sifting, not from a stratified layer. It has never been unfolded; the letters exist only in X-ray tomography.
  - Replacement **detail**: "A rectangular stone structure, about 9 × 7 m, with a ramp rather than steps (cf. Exod 20:26). It stands over an earlier round structure. Of the bones, 96% are from kosher animals; the other 4% include snake and tortoise. A folded lead object about 2 cm across was sifted from Zertal's spoil heap in 2019. Its publishers read 'Cursed… by the god YHW' in tomography scans; it has never been opened."
  - Replacement **status**: "Zertal read the structure as an altar, and Hawkins (2012) found it fits a cultic site. The lead object's inscription is disputed: Stripling, Galil et al. (2023) read 48 letters; Maeir & Rollston (IEJ 2023) and Haughwout (2024) say no letters are demonstrable; Mazar identifies it as a net sinker. As a spoil-heap find it has no stratified date."
- **[P]** citation "Zertal excavations; …" →
  - Replacement **citation**: "A. Zertal, Tel Aviv 13-14 (1986-87) 105-165. L. K. Horwitz, same volume, 173-189. S. Stripling, G. Galil et al., Heritage Science 11 (2023) 105. A. M. Maeir & C. Rollston, and A. Mazar, IEJ 73/2 (2023). M. S. Haughwout, Heritage Science 12 (2024) 70." URL: https://www.nature.com/articles/s40494-023-00920-9

## deir-alla-balaam  (record: deir-alla-inscription)
The content matches the record. The date (c. 800 BCE, from script and context), the site, and the title naming Balaam son of Beor, seer of the gods, all agree.
- **[S]** status "Accepted."
  - Replacement **status**: "Ink on wall plaster, found in fragments in 1967 by Franken's Dutch expedition. Combination I, line 1 names bl'm br b'r, 'Balaam son of Beor'. The text does not name Balak, Moab, Israel or YHWH, and its language (Aramaic or Canaanite) is argued."
- **[P]** citation "Deir Alla plaster inscription (1967)." (Wikipedia URL) →
  - Replacement **citation**: "J. Hoftijzer & G. van der Kooij, Aramaic Texts from Deir 'Alla (Brill 1976). Same editors, The Balaam Text from Deir 'Alla Re-Evaluated (1991). J. A. Hackett, The Balaam Text from Deir 'Alla (1980/84)." URL: https://doi.org/10.1163/9789004670327

## jeremiah-bullae  (record: jeremiah-bullae)
- **[C]** detail "…the last two found meters apart, in the 586 BCE destruction layer" → the record says Mykytiuk (Maarav 16/1, 2009: 94) states that the findspots of the Jehucal and Gedaliah bullae "lie in an archaeological context whose date is disputed". They are therefore dated by palaeography (late 7th-early 6th c.). Finkelstein et al. (Tel Aviv 34, 2007) dispute Mazar's dating of the Large Stone Structure. The record explicitly corrects the "586 BCE destruction layer" claim, and gives no distance between the two findspots. Source: https://doi.org/10.1086/mar200916105 ; https://doi.org/10.1179/tav.2007.2007.2.142
- **[U]** the Gedaliah patronym → the first letter of Pashhur is damaged. Mykytiuk argues for pe, "nun perhaps cannot be ruled out completely". He grades the Jehucal and Gedaliah matches "grade 2 or higher" (name plus patronym plus date; a third identifying mark is lacking) and Gemariah "grade 3".
  - Replacement **detail**: "Clay seal impressions of Gemaryahu son of Shaphan (Jer 36:10), from the 'House of the Bullae' hoard (Shiloh). Also Yehukal son of Shelemyahu (Jer 37:3) and Gedalyahu son of [P]ashhur (Jer 38:1), from Mazar's Large Stone Structure excavation. The last two are dated by letter forms to the late 7th-early 6th century; their findspot's date is disputed. The first letter of Pashhur is damaged."
- **[S]** status "Accepted."
  - Replacement **status**: "Mykytiuk (2009) grades the matches: Gemariah reliable (grade 3); Jehucal and Gedaliah reasonable (grade 2 or higher). Name, patronym and date fit, but no title or office is written."
- **[P]** citation "City of David bullae archive." with a madainproject.com URL → the record states that "is not a primary source".
  - Replacement **citation**: "Y. Shiloh & D. Tarler, Biblical Archaeologist 49 (1986) 196-209. E. Mazar, The Palace of King David (2009). L. J. Mykytiuk, Maarav 16/1 (2009) 49-132." URL: https://doi.org/10.1086/mar200916105

## amarna-letters  (record: amarna-letters)
- **[U]** detail quote "'The Habiru are capturing the fortresses of the king… if no archers come this year, all the lands of the king, my lord, are lost.'" → there is no letter number or translation given, and the quote does not match the record's verbatim text. The record's EA 286 (Abdi-Heba) in Barton's translation reads: "There are no lands left to the king, my lord. The Habiri plunder all the countries of the king. If there are mercenaries in this year, then there will be left countries of the king, my lord. If there are no mercenaries, the countries of the king will be lost." Source: Barton 1916 p. 346, https://archive.org/details/archaeologybible00bartuoft
  - Replacement quote: "'The Habiri plunder all the countries of the king. If there are mercenaries in this year, then there will be left countries of the king, my lord. If there are no mercenaries, the countries of the king will be lost.' (Abdi-Heba of Jerusalem, EA 286, tr. Barton 1916)"
- **[U]** confirms "…exactly as Joshua–Judges depicts it" and detail "The letters independently confirm the fragmented city-state Canaan of the conquest narratives" → the record says the letters "name no Israelite person or tribe". They show city-states "under Egyptian overlordship, complaining of Habiru raids". The Habiru are described by what they do; local rulers can side with them (EA 287). The match to Joshua-Judges is a reading.
  - Replacement **confirms**: "A Canaan of rival city-kings, among them a king at Jerusalem in the 14th century BCE, under Egyptian overlordship and complaining of Habiru raids"
- **[S]** status "Archive firmly accepted; …"
  - Replacement **status**: "Nearly 400 tablets found at Tell el-Amarna in 1887-88. Abdi-Heba's six Jerusalem letters (EA 285-290) are in Berlin. Whether the Habiru are the Hebrews is a reading; the letters describe them by what they do, not by descent."
- **[P]** citation "W. L. Moran, The Amarna Letters (1992)." → this is a translation. The record has the collation edition and museum numbers.
  - Replacement **citation**: "A. F. Rainey, The El-Amarna Correspondence (Brill 2015; collation of all extant tablets). EA 285-290 = VAT 1601, 1642, 1644, 1643, 1645+2709, 1646 (Berlin). Translations: Moran (1992); Lauinger & Yoder (2025)." URL: https://doi.org/10.1163/9789004281547

## bubastite-portal  (record: bubastite-portal)
- **[C]** detail "naming some 150 towns" → Breasted (ARE IV §718) counted 156 captive-ovals, but only about 75 names were legible by 1906. Rows 4 and 10 are almost entirely lost. Source: https://archive.org/details/ancientrecordsof0004jame_k7s1
- **[C]** detail "A fragment of his victory stele was excavated at Megiddo itself." → the fragment was noticed on a block thrown out by Schumacher's workmen, which had lain about twenty years on the mound. It was not excavated in place. Source: Breasted's foreword in Fisher, OIC 4 (1929), https://isac.uchicago.edu/research/publications/oic/oic-4-excavation-armageddon
- **[U]** detail "…matching the corridor the Bible says he struck when he 'came up against Jerusalem'" → Jerusalem is not among the surviving names. Breasted (1906 §717) held it "must have been lost in one of the lacunae"; in 1929 he said the list "does not mention it". No king of Judah is named, and Breasted rejected the old reading of No. 29 as "kingdom of Judah".
  - Replacement **detail**: "Shoshenq I (the Bible's Shishak) carved a triumph scene at Karnak: 156 name-rings, of which about 75 were still legible in 1906. They include Megiddo, Taanach, Beth-Shean, Gibeon, Aijalon and a long series of Negev places. Jerusalem is not among the surviving names; Breasted thought it lost in the damaged rows. A fragment of a Shoshenq stela was found among Schumacher's spoil at Megiddo."
- **[S]** status "Firmly accepted — …"
  - Replacement **status**: "Shoshenq's campaign is attested on the wall and by the Megiddo stela fragment. Its match to 1 Kings 14:25 rests on the name Shishak and the region. The list does not preserve Jerusalem, and whether it records one route or a composite is argued (Wilson 2005; Dodson 2023)."
- **[P]** citation "Bubastite Portal, Karnak; Megiddo stele fragment; …" →
  - Replacement **citation**: "Epigraphic Survey, Reliefs and Inscriptions at Karnak III: The Bubastite Portal (OIP 74, 1954). J. H. Breasted, Ancient Records of Egypt IV (1906) §§709-722. C. S. Fisher, The Excavation of Armageddon (OIC 4, 1929). cf. 1 Kings 14:25-26." URL: https://isac.uchicago.edu/research/publications/oip/reliefs-and-inscriptions-karnak-volume-iii-bubastite-portal

---

## Ark chapter: Durupınar card  (`ark-design.json` science.evidence[5]; record: durupinar)
The card does not contradict the record. The record does not list the university's 28 Aug 2026 release itself, so the radar wording was not checked. The ~40% carbon figure matches Arkeonews (23 Sep 2026). The card is outdated and one-sided on these points:
- **[U]** observation and notes are frozen at August 2026 → the season ran 29 Jun-11 Sep 2026. Cores went to 18 m inside and outside the formation. A drill bit broke on a hard layer at 4-5 m inside; Noah's Ark Scans' press release of 23 Sep suggested petrified wood, with no lab result. About 1,000 soil samples went to an Ankara lab, with results promised for winter 2026-27 and none released as of 27 Sep 2026. On 27 Sep 2026 the project director, Cenker Atila, called "definitively discovered" headlines misleading. The work is run with Noah's Ark Scans, which the card does not mention. Sources: https://www.globenewswire.com/news-release/2026/09/23/3367545/0/en/core-drilling-begins-at-durupinar-noah-s-ark-site-drill-bit-shatters-on-possible-layer-of-petrified-wood.html ; https://arkeonews.net/noahs-ark-mystery-deepens-as-new-discoveries-emerge-near-mount-ararat/ ; https://turkiyegorus.com/arastirma-ekibi-baskani-acikladi-nuhun-gemisi-bulundu-mu/
  - Replacement **observation**: "Sivas Cumhuriyet University (director Cenker Atila), working with Noah's Ark Scans, ran the first permitted coring season at the boat-shaped Durupınar formation from 29 June to 11 September 2026. Its August update reported straight-edged radar anomalies and about 40 percent more carbon in soil from inside the outline. Cores reached 18 m, and a drill bit broke on a hard layer at 4-5 m. About 1,000 samples are at an Ankara lab, with results promised for winter 2026-27."
- **[U]** the card gives only the investigation side. The record's rock evidence is not mentioned. The 1988 cores, drilled to 10 m, found "no evidence for wood, petrified or otherwise" and hit layered bedrock at about 5 m (Baumgardner). All 12 of Collins's thin sections of "petrified wood" were basalt or andesite, and the "iron bracket" is limonite (Collins & Fasold 1996; Collins, PSCF 68:4, 2016). The earlier 2024 Noah's Ark Scans soil ratios were never published, and the lab is unnamed. Source: https://www.asa3.org/ASA/PSCF/2016/PSCF12-16Collins.pdf ; https://tc8bfx57eu1msb72.public.blob.vercel-storage.com/articles/Durupinar-Core-Drilling-Locations-and-Results.pdf
  - Replacement **notes**: "The radar and carbon figures are preliminary, and no lab report has been published. Earlier cores (1988) reached bedrock and found no wood, and thin sections of the 'petrified wood' samples were volcanic rock (Collins 2016). Our reading: a ridge of bedrock under thin soil could by itself make the soil inside differ from the mudflow around it. The 2026 cores are the first samples able to test the formation directly."

---

## Count

- **Cards audited:** 30 (29 artifact cards plus the Durupınar card).
- **Cards needing any change:** 29.
  - Only tall-el-hammam is clean.
  - deir-alla-balaam needs only its status and citation changed.
- **Findings:** 114 in total.

| Tag | Count | Cards affected |
|---|---|---|
| [C] contradictions | 13 | soleb 1, mesha 1, kurkh 1, sennacherib 1, hezekiah-bulla 1, jehoiachin 1, bethesda 1, mt-ebal 3, jeremiah 1, bubastite 2 |
| [U] unsupported, overstated or outdated | 48 | |
| [S] authority-word status | 25 | 17 are bare "Accepted." or "Firmly accepted."; 8 more lead with an authority word or "standard reading" |
| [P] non-primary citation where the record has a primary | 28 | |

**The contradictions most worth fixing first:**
1. **Mesha:** the card says the House of David line was "confirmed by 2023 imaging". The record has no 2023 imaging and no confirmation: the 2019 and 2022 studies still split between David and Balak.
2. **Pool of Bethesda:** the card says "excavation revealed… five porticoes". No colonnades were found; the five porticoes are a reconstruction from John 5:2.
3. **Jeremiah bullae:** the card says they were found "in the 586 BCE destruction layer". Their context's date is disputed, and they are dated by letter forms.
4. **Hezekiah bulla:** the card says "found 2015". It was excavated in 2009 and announced in 2015.
5. **Mount Ebal:** the card says "only kosher" bones; the record gives 96%. The card also says "ABR (2022)" when the publication was 2023, and names the critics wrongly.
6. **Bubastite Portal:** the card gives "some 150 towns"; about 75 names are legible. It says the Megiddo stela fragment was "excavated"; it came from a spoil dump.
7. **Kurkh:** the card gives the site as "Assyria"; it was found in SE Turkey.
8. **Taylor Prism:** the citation merges the British Museum prism and the Chicago prism, which are two different objects.
9. **Jehoiachin:** the card says "Pergamon Museum"; the tablets belong to the Vorderasiatisches Museum, closed since 2023.
10. **Soleb:** the card says "reading not disputed", but the last sign is disputed.
