# REBUILD_NOTES.md — the-passport-page-of-a-countr-2-20261121-0318

## v3 fix round (applied 2026-11-21 ~12:30 WIB, after tester review)

Tester verdict was NOT SUBMITTABLE (yet): all three right-column
DEPARTED stamps bled off the page, and the MRZ composite check digit
was wrong (0, should be 8). Applied: (a) stamps scaled to 0.88 before
rotation, so the right column's visible edge lands near 987 px, inside
the 1003 px page border, with no canvas truncation and no column
overlap; (b) MRZ2 final character 0 → 8 (composite check digit
recomputed from the data: 538 mod 10 = 8); (c) MANU-ITI atoll dot
moved up (fy 0.72 → 0.64) so its label clears the chart caption;
(d) issuing-officer signature shortened (width 140 → 120) so its
flourish clears the date. Re-rendered + re-verified (see below).

## v2 fix round (applied 2026-11-21 ~11:05 WIB, after post-build review)

Applied, in order: (a) portrait — bun redrawn AFTER the head so it attaches to the
head edge, temple skin rounds break the straight hairline, cheek
shading softened to near-skin tone; (b) handwritten signature
scribbles added on the bearer line and the issuing-officer line
(deterministic, seeded); (c) stamps — New Zealand pair is now a
circular date-stamp (different form), all rectangular stamps got
deterministic ink-gap texture on their borders; (d) atoll chart —
4 atolls labelled (NUKU-MANU, LUMARA, MANU-ITI, TAVAKE), stray wave
arcs removed, compass rose added; (e) "EYES Brown" got its ruled line,
redundant MRZ micro-caption removed. A 7th "Lumara departure" stamp
was considered and REJECTED (no room at legible size in the corner).

Known weaknesses of v2 + concrete improvement ideas for a rebuild round
(before the 13:18 WIB deadline, if the dev rate comes back low, or for
the next competition of the same kind).

## Known weaknesses (v1, as built)

1. **Portrait is stylised flat-vector, not a photo.** The face is clean
   and reads as a passport photo at spread scale, but at close range it
   is visibly drawn (flat hair cap, simple eyes). A judge comparing
   against a photorealistic entry could mark criterion 4 down. The
   trade-off was deliberate: a drawn portrait keeps every pixel
   consistent with the holder data (age 35 at issue, 36 at the last
   stamp; Polynesian, frangipani, pandanus collar), while a generated photo risks gibberish features
   and mismatched age/ethnicity.
2. **Stamps are geometric, not rubber-stamp textured.** Clean double
   borders + anchor glyph. They read as stamps, but lack ink bleed,
   uneven pressure, and fibre texture. No stamp overlaps the spine or
   another stamp in a messy real-world way (all neatly gridded).
3. **The atoll chart is schematic.** Nine dots + waves; it fills the
   space but is the least document-like element on the left page.
   The "LUMARA" dot is the only labelled atoll besides NUKU-MANU.
4. **Signature line is empty.** Real passports carry a bearer
   signature; ours has a blank ruled line. A handwritten-style
   signature (drawn as a bezier scribble) would add realism.
5. **MRZ band has a redundant caption.** The "P<KV · KV2847163 ·
   KAVARA" micro-line under the MRZ adds nothing; the space could
   hold a "MACHINE READABLE ZONE" label or be removed.
6. **No wear/age.** The spread looks freshly printed: no creases,
   no thumbprint smudges, no slightly uneven inking. Real documents
   have small imperfections; ours has none.

## Concrete rebuild ideas (ranked)

1. **Rubber-stamp texture pass:** after rotating each stamp, apply a
   low-alpha noise mask (deterministic seeded noise) and erase a few
   small random-looking chips from the border, so ink looks stamped
   rather than printed. Keep text fully legible — texture only on
   borders/fill, never over glyphs.
2. **Handwritten signature:** draw "Mereana S. Tavake" as a connected
   bezier scribble on the signature line, dark blue-black ink, slight
   slant. Also add the issuing officer's signature scribble above
   "Issuing officer, Lumara".
3. **Paper grain + faint guilloche:** overlay a very light deterministic
   noise + fine wavy guilloche lines across both pages (alpha ~8–12)
   to kill the flat-digital look. Must stay subtle — legibility first.
4. **Atoll chart upgrade:** replace dots with tiny atoll outlines
   (ring shapes with a lagoon dot), add a compass rose, and label 3–4
   atolls instead of 2. Keep the caption clear of the wave arcs.
5. **Stamp overlap:** shift the second stamp of each pair 6–10px so
   its edge crosses the first stamp's border, as real consecutive
   stamps do. Keep all text unobstructed.
6. **Portrait shading pass:** add a soft radial shadow under the chin
   and a subtle highlight on the cheekbones (flat ellipses at low
   alpha) to give the face a little more depth without going uncanny.
7. **MRZ tidy:** drop the micro-caption line; vertically centre the
   two MRZ lines in the band.
8. **Second telling detail (if criterion 5 needs more):** add a small
   "VALID FOR SEA PASSAGE ONLY" visa-condition line in the remarks
   block in Kavaran (invented language) + English, e.g.
   "FOLAU VAKA PE — SEA PASSAGE ONLY".

## What NOT to change

- The dataset (names, dates, MRZ, stamp chronology) — all verified
  internally consistent; any field change must recompute the MRZ
  check digits (ICAO 9303, weights 7-3-1).
- The palette (navy / black / red on cream) and the Liberation-only
  font discipline — the layout coherence is the entry's main strength.
- The sea-only concept — it is what makes the travel history and the
  endorsement corroborate each other. Never add a plane, an airport
  code, or a flight number.
