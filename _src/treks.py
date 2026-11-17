"""Trek journal content for babypanda.top.

Edit this file, then run `python _src/build.py` from the repo root.

- "num" is the Baby Panda Trek (BPT) number, in the order we did them.
- "date" only where a trip poster showed it; otherwise None (no guessing).
- "at" is an approximate (lat, lon) for the map; None leaves the trek off the map.
- Treks we have little written about stay short on purpose. Add stories as you go.
"""

IG = "https://www.instagram.com/babypanda.top/"


def reel(code):
    return f"{IG}reel/{code}/"


_TREKS = [
    {
        "num": 18, "slug": "gundar-zero-point", "name": "Gundar Zero Point",
        "at": (10.232, 77.465), "place": "Kodaikanal, Tamil Nadu", "range": "Palani Hills",
        "kind": "Forest trail", "date": "2026-11-02", "hue": "leaf",
        "summary": "A forest walk out from the Solar Observatory into the streams of the upper Palani Hills.",
        "body": [
            "Our eighteenth trek, and our first in the Palani Hills. We started at the Kodaikanal Solar Observatory, high on the hill above the town, and headed down into the shola forest toward Gundar Zero Point.",
            "The trail trades the crowds of Kodaikanal's lake and viewpoints for quiet forest, cold streams and rocks you'll want to stop on. Expect mist, wet ground and sudden changes in light, even outside the monsoon.",
            "Trails like this one are exactly why we're building Thadam: in the Palani Hills there's rarely mobile signal, and published distances and start points are often wrong.",
        ],
        "facts": [("Start", "Kodaikanal Solar Observatory"), ("Region", "Palani Hills, Dindigul district"),
                  ("Terrain", "Shola forest, streams, rock"), ("Pack", "Rain layer, grippy shoes, warm top")],
        "links": [("Watch the trek", reel("DfPrEISqbKA")), ("Trip announcement", reel("DfKmX4JKIM7"))],
    },
    {
        "num": 17, "slug": "mangi-tungi", "name": "Mangi Tungi",
        "at": (20.94, 73.99), "place": "Nashik, Maharashtra", "range": "Sahyadris",
        "kind": "Twin pinnacles", "date": "2026-10-24", "hue": "rock",
        "summary": "Two rock pinnacles joined by a saddle, with Jain cave temples cut into the cliffs.",
        "body": [
            "Mangi and Tungi are twin pinnacles in Nashik district's Sahyadris, linked by a narrow saddle. They're a major Jain pilgrimage site, with temples and carvings cut into the rock faces of both peaks.",
            "The climb is a long stone stairway rather than a scramble, but it's relentless, and the views open up across the plateau as you rise. At the base stands the 108-foot Statue of Ahimsa of Rishabhanatha, carved from the hill itself.",
            "Go early. The stairs are exposed, and the rock heats up quickly on clear days.",
        ],
        "facts": [("Nearest village", "Tahrabad, Satana taluka"), ("Region", "Sahyadris, Nashik district"),
                  ("Terrain", "Stone stairs, rock-cut temples"), ("Pack", "Water, sun cap, socks for temple areas")],
        "links": [("Watch the trek", reel("DeznHnCxT8i"))],
    },
    {
        "num": 16, "slug": "tada-falls", "name": "Tada Falls",
        "at": (13.60, 79.83), "place": "Tirupati district, Andhra Pradesh", "range": "Eastern Ghats",
        "kind": "Waterfall", "date": "2026-08-23", "hue": "water",
        "summary": "A forest walk along a stream to Ubbalamadugu, a waterfall dropping into a clear green pool.",
        "body": [
            "Tada Falls, also called Ubbalamadugu, sits in the Eastern Ghats forest near the Andhra–Tamil Nadu border, close enough to Chennai for a day trip.",
            "The walk follows a rocky stream bed through the forest, crossing the water again and again before the cliffs close in and the falls appear at the end. Its pool is clear and green, ringed by red rock.",
            "Entry is through the forest department checkpoint, so plan around its hours. After heavy rain the crossings get fast; turn back if the water looks wrong.",
        ],
        "facts": [("Also called", "Ubbalamadugu Falls"), ("Region", "Eastern Ghats, near Sri City"),
                  ("Terrain", "Stream bed, boulders, crossings"), ("Pack", "Sandals with grip, dry bag, change of clothes")],
        "links": [("Trip announcement", reel("DcJlVfNJIeV"))],
    },
    {
        "num": 15, "slug": "sinhagad-fort", "name": "Sinhagad Fort",
        "at": (18.366, 73.755), "place": "Pune, Maharashtra", "range": "Sahyadris",
        "kind": "Hill fort", "date": None, "hue": "fort",
        "summary": "The Lion Fort above Pune, won back in 1670 at the cost of Tanaji Malusare's life.",
        "body": [
            "Sinhagad stands about 30 km southwest of Pune, at 1,312 m. It was once called Kondhana, and is remembered for the 1670 battle in which the Maratha commander Tanaji Malusare died retaking it. Shivaji Maharaj is said to have mourned: “The fort is won, but the lion is lost.”",
            "The trail climbs steadily up the hillside to the walls, then wanders between gates, bastions and old water tanks on top. In the monsoon the whole hill turns green and the fort disappears into cloud.",
        ],
        "facts": [("Height", "1,312 m"), ("Open", "Daily, 6:00 AM to 6:00 PM"),
                  ("Best time", "June to February; July to September for mist"), ("From Pune", "About 1 to 1.5 hours by road")],
        "links": [("Watch the trek", reel("DcH_UqdJzZT"))],
    },
    {
        "num": 14, "slug": "moola-kona-falls", "name": "Moola Kona Waterfall",
        "at": (13.37, 79.55), "place": "Tirupati district, Andhra Pradesh", "range": "Eastern Ghats",
        "kind": "Waterfall", "date": None, "hue": "water",
        "summary": "A day of Andhra forest falls, from a hidden rock pool to Kailasakona beside its temple.",
        "body": [
            "This trek took us to the Eastern Ghats near the Andhra–Tamil Nadu border for a day of waterfalls: Moola Kona, the small rock pool at Thotti Kona, and Kailasakona beside its temple.",
            "Thotti Kona is a hidden fall and natural rock pool just before Kailasakona, about 110 to 120 km from Chennai. “Thotti” means tub or basin, and that's what it is: a compact pool with water dropping into it from a short height. It's quieter than the temple falls nearby.",
            "Kailasakona, or Kaulesha Kona, is about 40 feet high, in Narayanavanam mandal, with a temple to Shiva and Parvati beside it. From the car park on the Uttukottai–Puttur–Tirupati road (NH 40), a stepped path, lit at night, reaches the main falls in three to five minutes. On the way in there are two smaller falls, 4 to 6 feet high.",
            "The Moola Kona reel has a song in it. Watch to the end.",
        ],
        "facts": [("Falls visited", "Moola Kona, Thotti Kona, Kailasakona"), ("Kailasakona height", "About 40 ft"),
                  ("From Chennai", "About 110 to 120 km"), ("Best time", "October to March, when the flow is steady")],
        "links": [("Watch Moola Kona", reel("DcF13kzJDD1")), ("Kailasakona", reel("DcFg0YrJUnL")), ("Thotti Kona", reel("DcFu2MBpEGI"))],
    },
    {
        "num": 13, "slug": "kataldhar-falls", "name": "Kataldhar Waterfall",
        "at": (18.79, 73.38), "place": "Near Lonavla, Maharashtra", "range": "Sahyadris",
        "kind": "Waterfall", "date": None, "hue": "water",
        "summary": "A monsoon waterfall in a rock bowl, reached on foot through forest below Lonavla.",
        "body": [
            "Kataldhar is a monsoon waterfall that pours into a rock bowl in the forest below Lonavla. There's no road to it; you reach it on foot, down through the trees and over wet rock.",
            "The descent is steep and slippery in the rain, and it's an even steeper climb back out. It's worth it once you're standing under the falls.",
        ],
        "facts": [("Region", "Sahyadris, near Lonavla"), ("Season", "Monsoon, July to September"),
                  ("Terrain", "Forest, steep wet rock"), ("Pack", "Gloves, shoes with deep grip, spare clothes")],
        "links": [("See the highlights", IG)],
    },
    {
        "num": 12, "slug": "sandhan-valley", "name": "Sandhan Valley",
        "at": (19.52, 73.72), "place": "Bhandardara, Maharashtra", "range": "Sahyadris",
        "kind": "Canyon", "date": None, "hue": "rock",
        "summary": "The Valley of Shadows: a narrow canyon cut by water, deep enough to block out the sun.",
        "body": [
            "Sandhan Valley, near Samrad village in the Bhandardara region, is a narrow canyon carved by water through the Sahyadri basalt. The walls are close and tall enough that much of it stays in shade all day, hence the name Valley of Shadows.",
            "The route squeezes between the walls over boulders and through pools, some of them waist-deep. It's a trek to do after the monsoon, once the water has dropped; during heavy rain the canyon is dangerous.",
        ],
        "facts": [("Base village", "Samrad, near Bhandardara"), ("Region", "Sahyadris, Ahilyanagar district"),
                  ("Best time", "After the monsoon, October onward"), ("Terrain", "Boulders, pools, narrow passages")],
        "links": [("See the highlights", IG)],
    },
    {
        "num": 11, "slug": "aare-falls", "name": "Aare Falls",
        "at": None, "place": "Maharashtra", "range": "Sahyadris",
        "kind": "Waterfall", "date": None, "hue": "water",
        "summary": "A Sahyadri monsoon waterfall, and trek number eleven.",
        "body": [
            "Aare Falls was our eleventh trek: a walk out to a monsoon waterfall in the Sahyadris.",
            "We'll add the full story and photos from this one soon.",
        ],
        "facts": [("Region", "Sahyadris"), ("Type", "Monsoon waterfall"),
                  ("Pack", "Rain layer, shoes with grip, spare clothes")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 10, "slug": "katraj-to-sinhagad", "name": "K2S: Katraj to Sinhagad",
        "at": (18.40, 73.83), "place": "Pune, Maharashtra", "range": "Sahyadris",
        "kind": "Ridge traverse", "date": None, "hue": "leaf",
        "summary": "Pune's classic long ridge walk, hill after hill from Katraj Ghat to the walls of Sinhagad.",
        "body": [
            "K2S is the long ridge walk from Katraj Ghat to Sinhagad along the hills south of Pune. It's less a single climb than a string of them: up one hill, down, and up the next, again and again.",
            "It's a test of stamina more than technique. Pace yourself, carry more water than you think you need, and save something for the final climb to Sinhagad.",
        ],
        "facts": [("Start", "Katraj Ghat, Pune"), ("Finish", "Sinhagad Fort"),
                  ("Terrain", "Repeated ascents and descents on a ridge"), ("Pack", "Extra water, head torch, snacks")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 9, "slug": "nathbaba-caves", "name": "Nathbaba Caves",
        "at": None, "place": "Maharashtra", "range": "Sahyadris",
        "kind": "Caves", "date": None, "hue": "rock",
        "summary": "A trek to rock caves in the Sahyadris, our ninth.",
        "body": [
            "Nathbaba Caves was our ninth trek, out to caves in the Sahyadri rock.",
            "We'll add the full story and photos from this one soon.",
        ],
        "facts": [("Region", "Sahyadris"), ("Type", "Caves"),
                  ("Pack", "Head torch, water, shoes with grip")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 8, "slug": "kalu-waterfall", "name": "Kalu Waterfall",
        "at": (19.30, 73.75), "place": "Malshej Ghat, Maharashtra", "range": "Sahyadris",
        "kind": "Waterfall", "date": None, "hue": "water",
        "summary": "A tall monsoon waterfall in the Malshej region, falling off the edge of the plateau.",
        "body": [
            "Kalu Waterfall drops off the edge of the Sahyadri plateau in the Malshej region, and in full monsoon it's one of the taller falls in Maharashtra.",
            "The walk in crosses farmland and streams, and the trail gets muddy fast. On a misty day you'll hear the falls long before you see them.",
        ],
        "facts": [("Region", "Sahyadris, Malshej Ghat area"), ("Season", "Monsoon, July to September"),
                  ("Terrain", "Fields, streams, mud"), ("Pack", "Poncho, shoes with deep grip")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 7, "slug": "karnala-fort", "name": "Karnala Fort",
        "at": (18.88, 73.12), "place": "Panvel, Maharashtra", "range": "Sahyadris",
        "kind": "Hill fort", "date": None, "hue": "fort",
        "summary": "A fort crowned by a thumb-shaped rock pinnacle, inside the Karnala Bird Sanctuary.",
        "body": [
            "Karnala Fort rises above the Mumbai–Goa highway near Panvel, easy to spot by the thumb-shaped pinnacle of rock on its summit. The trail runs through the Karnala Bird Sanctuary, so the forest is loud with birds in the mornings.",
            "It's a good first fort: a steady forest climb, a few rocky steps near the top, and wide views over the Konkan plains.",
        ],
        "facts": [("Near", "Panvel, Raigad district"), ("Trail", "Through Karnala Bird Sanctuary"),
                  ("Landmark", "Thumb-shaped summit pinnacle"), ("Pack", "Water, light snacks, binoculars")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 6, "slug": "harishchandragad", "name": "Harishchandragad",
        "at": (19.39, 73.78), "place": "Ahilyanagar, Maharashtra", "range": "Sahyadris",
        "kind": "Hill fort", "date": None, "hue": "rock",
        "summary": "The great Sahyadri fort: Konkan Kada's sheer cliff, an ancient cave temple and Taramati peak.",
        "body": [
            "Harishchandragad is one of the best-loved treks in the Sahyadris. On top you'll find the Harishchandreshwar temple, the Kedareshwar cave with its Shiva linga standing in water, and Konkan Kada, a vast concave cliff that drops away toward the Konkan.",
            "The climb is long and the plateau is big. Give yourself time on top, and if the clouds lift at Konkan Kada, stay and watch.",
        ],
        "facts": [("Highlights", "Konkan Kada, Kedareshwar cave, Taramati"), ("Region", "Sahyadris, Ahilyanagar district"),
                  ("Terrain", "Long climb, rock patches, large plateau"), ("Pack", "Extra water, warm layer, head torch")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 5, "slug": "tahuli-peak", "name": "Tahuli Peak",
        "at": (19.17, 73.20), "place": "Near Kalyan, Maharashtra", "range": "Sahyadris",
        "kind": "Peak", "date": None, "hue": "leaf",
        "summary": "A quiet peak near Kalyan with rock pinnacles on top and long views over the plains.",
        "body": [
            "Tahuli sits in the hills near Kalyan and Ambernath, a short trip from Mumbai but far quieter than the famous forts. Rock pinnacles stand on its summit plateau.",
            "The trail climbs through grass and scrub with few shady stretches, so start early and carry plenty of water.",
        ],
        "facts": [("Near", "Kalyan and Ambernath"), ("Region", "Sahyadris, Thane district"),
                  ("Terrain", "Grass slopes, rocky summit"), ("Pack", "Plenty of water, sun cap")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 4, "slug": "peb-fort", "name": "Peb Fort",
        "at": (19.02, 73.29), "place": "Near Neral, Maharashtra", "range": "Sahyadris",
        "kind": "Hill fort", "date": None, "hue": "fort",
        "summary": "Vikatgad: a fort below Matheran, reached by ladders and a narrow ledge on the rock face.",
        "body": [
            "Peb Fort, also called Vikatgad, sits on the range just north of Matheran. The final approach is the fun part: iron ladders and a narrow ledge along the rock face lead you up to the top.",
            "From the summit you look across at Matheran's plateau and down to the plains. Take the exposed sections slowly, especially when the rock is wet.",
        ],
        "facts": [("Also called", "Vikatgad"), ("Near", "Neral and Matheran"),
                  ("Terrain", "Forest trail, ladders, rock ledge"), ("Pack", "Gloves, shoes with grip, water")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 3, "slug": "garbett-plateau", "name": "Garbett Plateau",
        "at": (19.03, 73.30), "place": "Matheran range, Maharashtra", "range": "Sahyadris",
        "kind": "Plateau", "date": None, "hue": "leaf",
        "summary": "A wide, grassy plateau at the north end of the Matheran range, open to the sky.",
        "body": [
            "Garbett Plateau stretches out from the northern end of the Matheran range: a long, open tableland of grass with drops on either side and views across the valleys.",
            "In the monsoon it's at its greenest, with clouds pouring over the edges. The climb up is steady, and the walk across the top is the reward.",
        ],
        "facts": [("Region", "Matheran range, Raigad district"), ("Season", "Best in and after the monsoon"),
                  ("Terrain", "Climb, then open plateau"), ("Pack", "Rain layer, water, snacks")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 2, "slug": "sondai-fort", "name": "Sondai Fort",
        "at": (18.93, 73.30), "place": "Near Karjat, Maharashtra", "range": "Sahyadris",
        "kind": "Hill fort", "date": None, "hue": "fort",
        "summary": "A small fort near Karjat with a short climb, a ladder near the top and rock-cut water cisterns.",
        "body": [
            "Sondai is a small fort near Karjat: a short, friendly climb that makes a good first trek. Near the top a ladder helps you up the last rock step.",
            "On the summit you'll find old rock-cut water cisterns and views across to Matheran and the Morbe dam.",
        ],
        "facts": [("Near", "Karjat, Raigad district"), ("Terrain", "Short climb, ladder near the top"),
                  ("Good for", "First-time trekkers"), ("Pack", "Water, shoes with grip")],
        "links": [("Follow for photos", IG)],
    },
    {
        "num": 1, "slug": "katildhar", "name": "Katildhar",
        "at": None, "place": "Maharashtra", "range": "Sahyadris",
        "kind": "Monsoon trek", "date": None, "hue": "leaf",
        "summary": "Where Baby Panda Treks began: trek number one.",
        "body": [
            "Katildhar was our very first trek, the trip that started it all, out in the Sahyadris.",
            "We'll add the full story and photos from this one soon.",
        ],
        "facts": [("Trek", "Our first"), ("Region", "Sahyadris"), ("Type", "Day trek"),
                  ("Pack", "Rain layer, shoes with grip, spare clothes")],
        "links": [("Follow for photos", IG)],
    },
]

TREKS = sorted(_TREKS, key=lambda t: -t["num"])
