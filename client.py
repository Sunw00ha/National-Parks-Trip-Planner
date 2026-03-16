# client-side
# Names: Irene Ha, Ejean Kuo, Henron Ruan

import requests
import pathlib
import sys
import json

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

park_map = {
    "ABLI": "Abraham Lincoln Birthplace National Historical Park",
    "ACAD": "Acadia National Park",
    "ADAM": "Adams National Historical Park",
    "AFAM": "African American Civil War Memorial",
    "AFBG": "African Burial Ground National Monument",
    "AGFO": "Agate Fossil Beds National Monument",
    "ALKA": "Ala Kahakai National Historic Trail",
    "ALAG": "Alagnak Wild River",
    "AKR": "Alaska Region",
    "AKRO": "Alaska Regional Office",
    "ALCA": "Alcatraz Island",
    "ALEU": "Aleutian World War II National Historic Area",
    "ALFL": "Alibates Flint Quarries National Monument",
    "ALPO": "Allegheny Portage Railroad National Historic Site",
    "AMCH": "Amache National Historic Site",
    "AMME": "American Memorial Park",
    "AMIS": "Amistad National Recreation Area",
    "ANAC": "Anacostia Park",
    "ANDE": "Andersonville National Historic Site",
    "ANJO": "Andrew Johnson National Historic Site",
    "ANIA": "Aniakchak National Monument and Preserve",
    "ANTI": "Antietam National Battlefield",
    "APIS": "Apostle Islands National Lakeshore",
    "APHN": "Appalachian Highlands Network",
    "APPA": "Appalachian National Scenic Trail",
    "APCO": "Appomattox Court House National Historical Park",
    "ARMO": "Arabia Mountain National Heritage Area",
    "ARCH": "Arches National Park",
    "ARCN": "Arctic Network",
    "ARPO": "Arkansas Post National Memorial",
    "ARHO": "Arlington House, The Robert E. Lee Memorial",
    "ASIS": "Assateague Island National Seashore",
    "ATTR": "Atchafalaya National Heritage Area",
    "AUCA": "Augusta Canal National Heritage Area",
    "AZRU": "Aztec Ruins National Monument",
    "BADL": "Badlands National Park",
    "BALT": "Baltimore National Heritage Area",
    "BAWA": "Baltimore-Washington Parkway",
    "BAND": "Bandelier National Monument",
    "BEPA": "Belmont-Paul Women's Equality National Monument",
    "BEOL": "Bent's Old Fort National Historic Site",
    "BELA": "Bering Land Bridge National Preserve",
    "BIBE": "Big Bend National Park",
    "BICY": "Big Cypress National Preserve",
    "BIHO": "Big Hole National Battlefield",
    "BISO": "Big South Fork National River and Recreation Area",
    "BITH": "Big Thicket National Preserve",
    "BICA": "Bighorn Canyon National Recreation Area",
    "BICR": "Birmingham Civil Rights National Monument",
    "BISC": "Biscayne National Park",
    "BLCA": "Black Canyon Of The Gunnison National Park",
    "BLRV": "Blackstone River Valley National Historical Park",
    "BLSC": "Blackwell School National Historic Site",
    "BLRN": "Blue Ridge National Heritage Area",
    "BLRI": "Blue Ridge Parkway",
    "BLUE": "Bluestone National Scenic River",
    "BOWA": "Booker T. Washington National Monument",
    "BOAF": "Boston African American National Historic Site",
    "BOHA": "Boston Harbor Islands National Recreation Area",
    "BOST": "Boston National Historical Park",
    "BRCR": "Brices Cross Roads National Battlefield Site",
    "BRVB": "Brown v. Board Of Education National Historic Site",
    "BRCA": "Bryce Canyon National Park",
    "BUIS": "Buck Island Reef National Monument",
    "BUFF": "Buffalo National River",
    "CABR": "Cabrillo National Monument",
    "CALA": "Cache la Poudre River National Heritage Area",
    "CALI": "California National Historic Trail",
    "CANE": "Camp Nelson National Monument",
    "CANA": "Canaveral National Seashore",
    "CARI": "Cane River Creole National Historical Park",
    "CRHA": "Cane River National Heritage Area",
    "CACH": "Canyon de Chelly National Monument",
    "CANY": "Canyonlands National Park",
    "CACO": "Cape Cod National Seashore",
    "CAHA": "Cape Hatteras National Seashore",
    "CAKR": "Cape Krusenstern National Monument",
    "CALO": "Cape Lookout National Seashore",
    "CAHI": "Capitol Hill Parks",
    "CARE": "Capitol Reef National Park",
    "CAJO": "Captain John Smith Chesapeake National Historic Trail",
    "CAVO": "Capulin Volcano National Monument",
    "CARL": "Carl Sandburg Home National Historic Site",
    "CAVE": "Carlsbad Caverns National Park",
    "CAWO": "Carter G. Woodson Home National Historic Site",
    "CAGR": "Casa Grande Ruins National Monument",
    "CASA": "Castillo de San Marcos National Monument",
    "CACL": "Castle Clinton National Monument",
    "CAMO": "Castle Mountains National Monument",
    "CATO": "Catoctin Mountain Park",
    "CEBR": "Cedar Breaks National Monument",
    "CEBE": "Cedar Creek and Belle Grove National Historical Park",
    "CAKN": "Central Alaska Network",
    "CECH": "César E. Chávez National Monument",
    "CHCU": "Chaco Culture National Historical Park",
    "CHAM": "Chamizal National Memorial",
    "CHVA": "Champlain Valley National Heritage Partnership",
    "CHIS": "Channel Islands National Park",
    "CHPI": "Charles Pinckney National Historic Site",
    "CHYO": "Charles Young Buffalo Soldiers National Monument",
    "CHAT": "Chattahoochee River National Recreation Area",
    "CHOH": "Chesapeake and Ohio Canal National Historical Park",
    "CHBA": "Chesapeake Bay Gateways",
    "CHCH": "Chickamauga and Chattanooga National Military Park",
    "CHIC": "Chickasaw National Recreation Area",
    "CHDN": "Chihuahuan Desert Network",
    "CHIR": "Chiricahua National Monument",
    "CHRI": "Christiansted National Historic Site",
    "CIRO": "City Of Rocks National Reserve",
    "CLBA": "Clara Barton National Historic Site",
    "CLMO": "Claude Moore Colonial Farm",
    "COLO": "Colonial National Historical Park",
    "COLM": "Colorado National Monument",
    "COLT": "Coltsville National Historical Park",
    "CONG": "Congaree National Park",
    "COGA": "Constitution Gardens",
    "CORO": "Coronado National Memorial",
    "COWP": "Cowpens National Battlefield",
    "CRLA": "Crater Lake National Park",
    "CRMO": "Craters Of The Moon National Monument and Preserve",
    "CUGA": "Cumberland Gap National Historical Park",
    "CUIS": "Cumberland Island National Seashore",
    "CUPN": "Cumberland Piedmont Network",
    "CURE": "Curecanti National Recreation Area",
    "CUVA": "Cuyahoga Valley National Park",
    "DABE": "David Berger National Memorial",
    "DAAV": "Dayton Aviation Heritage National Historical Park",
    "DESO": "De Soto National Memorial",
    "DEVA": "Death Valley National Park",
    "DELE": "Delaware and Lehigh National Heritage Corridor",
    "DEWA": "Delaware Water Gap National Recreation Area",
    "DENA": "Denali National Park & Preserve",
    "DSC": "Denver Service Center",
    "DEPO": "Devils Postpile National Monument",
    "DETO": "Devils Tower National Monument",
    "DINO": "Dinosaur National Monument",
    "DRTO": "Dry Tortugas National Park",
    "DDEM": "Dwight D. Eisenhower Memorial",
    "EML": "Eastern Museum Laboratory",
    "EODC": "Eastern Office of Design and Construction",
    "ERMN": "Eastern Rivers and Mountains Network",
    "EBLA": "Ebey’s Landing National Historical Reserve",
    "EDAL": "Edgar Allan Poe National Historic Site",
    "EFMO": "Effigy Mounds National Monument",
    "EISE": "Eisenhower National Historic Site",
    "ELTE": "El Camino Real de los Tejas National Historic Trail",
    "ELCA": "El Camino Real de Tierra Adentro National Historic Trail",
    "ELMA": "El Malpais National Monument",
    "ELMO": "El Morro National Monument",
    "ELRO": "Eleanor Roosevelt National Historic Site",
    "TILLE": "Emmett Till and Mamie Till-Mobley National Monument",
    "ERIE": "Erie Canalway National Heritage Cooridor",
    "EUON": "Eugene O'Neill National Historic Site",
    "EVER": "Everglades National Park",
    "FATI": "Fallen Timbers Battlefield and Fort Miamis National Historic Site",
    "FEHA": "Federal Hall National Memorial",
    "FIIS": "Fire Island National Seashore",
    "FILA": "First Ladies National Historic Site",
    "FRST": "First State National Historical Park",
    "FLNI": "Flight 93 National Memorial",
    "FLFO": "Florissant Fossil Beds National Monument",
    "FOTH": "Ford's Theatre National Historic Site",
    "FOBO": "Fort Bowie National Historic Site",
    "FODA": "Fort Davis National Historic Site",
    "FODO": "Fort Donelson National Battlefield",
    "FODU": "Fort Dupont Park",
    "FOFO": "Fort Foote Park",
    "FOFR": "Fort Frederica National Monument",
    "FOLA": "Fort Laramie National Historic Site",
    "FOLS": "Fort Larned National Historic Site",
    "FOMA": "Fort Matanzas National Monument",
    "FOMC": "Fort McHenry National Monument and Historic Shrine",
    "FOMR": "Fort Monroe National Monument",
    "FONE": "Fort Necessity National Battlefield",
    "FOPO": "Fort Point National Historic Site",
    "FOPU": "Fort Pulaski National Monument",
    "FORA": "Fort Raleigh National Historic Site",
    "FOSC": "Fort Scott National Historic Site",
    "FOSM": "Fort Smith National Historic Site",
    "FOST": "Fort Stanwix National Monument",
    "FOSU": "Fort Sumter and Fort Moultire Historical Park",
    "FOUN": "Fort Union National Monument",
    "FOUS": "Fort Union Trading Post National Historic Site",
    "FOVA": "Fort Vancouver National Historic Site",
    "FOWA": "Fort Washington Park",
    "FOBU": "Fossil Butte National Monument",
    "FDRM": "Franklin Delano Roosevelt Memorial",
    "FRDE": "Franklin Delano Roosevelt National Memorial",
    "FRDO": "Frederick Douglass National Historic Site",
    "FRLA": "Frederick Law Olmsted National Historic Site",
    "FRSP": "Fredericksburg & Spotsylvania National Military Park",
    "FRRI": "Freedom Riders National Monument",
    "FRWA": "Freedom's Way National Heritage Area",
    "FRHI": "Friendship Hill National Historic Site",
    "GAAR": "Gates of the Arctic National Park & Preserve",
    "JEFF": "Gateway Arch National Park",
    "GATE": "Gateway National Recreation Area",
    "GARI": "Gauley River National Recreation Area",
    "GEGR": "General Grant National Memorial",
    "GERO": "George Rogers Clark National Historical Park",
    "GEWA": "George Washington Birthplace National Monument",
    "GWCA": "George Washington Carver National Monument",
    "GWMP": "George Washington Memorial Parkway",
    "GETT": "Gettysburg National Military Park",
    "GICL": "Gila Cliff Dwellings National Monument",
    "GLBA": "Glacier Bay National Park & Preserve",
    "GLAC": "Glacier National Park",
    "GLCA": "Glen Canyon National Recreation Area",
    "GLEC": "Glen Echo Park",
    "GLDE": "Gloria Dei Church National Historic Site",
    "GOGA": "Golden Gate National Recreation Area",
    "GOSP": "Golden Spike National Park",
    "GOIS": "Governors Island National Monument",
    "GRCA": "Grand Canyon National Park",
    "GRPO": "Grand Portage National Monument",
    "GRTE": "Grand Teton National Park",
    "GRKO": "Grant-Kohrs Ranch National Historic Site",
    "GRBA": "Great Basin National Park",
    "GREG": "Great Egg Harbor River",
    "GRFA": "Great Falls Park",
    "GLKN": "Great Lakes Network",
    "GRSA": "Great Sand Dunes National Park & Preserve",
    "GRSM": "Great Smoky Mountains National Park",
    "GRYN": "Greater Yellowstone Network",
    "GRSP": "Green Springs National Historic Landmark District",
    "GREE": "Greenbelt Park",
    "GUMO": "Guadalupe Mountains National Park",
    "GUCO": "Guilford Courthouse National Military Park",
    "GULN": "Gulf Coast Network",
    "GUIS": "Gulf Islands National Seashore",
    "GUGE": "Gullah/Geechee Cultural Heritage Corridor",
    "HAFO": "Hagerman Fossil Beds National Monument",
    "HALE": "Haleakalā National Park",
    "HAGR": "Hamilton Grange National Memorial",
    "HAMP": "Hampton National Historic Site",
    "HAHA": "Harmony Hall",
    "HFC": "Harpers Ferry Center",
    "HAFE": "Harpers Ferry National Historical Park",
    "HART": "Harriet Tubman National Historical Park",
    "HATU": "Harriet Tubman Underground Railroad National Historical Park",
    "HSTR": "Harry S. Truman National Historic Site",
    "HAVO": "Hawai'i Volcanoes National Park",
    "HTLN": "Heartland Network",
    "HEHO": "Herbert Hoover National Historic Site",
    "JAME": "Historic Jamestowne",
    "PIMA": "Hohokam-Pima National Monument",
    "HOFR": "Home Of Franklin D. Roosevelt National Historic Site",
    "HOME": "Homestead National Monument of America",
    "HONO": "Honouliuli Historic Site",
    "HOCU": "Hopewell Culture National Historical Park",
    "HOFU": "Hopewell Furnace National Historic Site",
    "HOVI": "Hopewell Village National Historic Site",
    "HOAL": "Horace Albright Training Center",
    "HOBE": "Horseshoe Bend National Military Park",
    "HOSP": "Hot Springs National Park",
    "HOVE": "Hovenweep National Monument",
    "HUTR": "Hubbell Trading Post National Historic Site",
    "HURV": "Hudson River Valley National Heritage Area",
    "IATR": "Ice Age National Scenic Trail",
    "ILMI": "Illinois and Michigan Canal National Heritage Corridor",
    "INDE": "Independence National Historical Park",
    "INDU": "Indiana Dunes National Park",
    "IMR": "Intermountain Region",
    "IMRO": "Intermountain Regional Office",
    "INUPI": "Iñupiat Heritage Center",
    "ISRO": "Isle Royale National Park",
    "JAGA": "James A. Garfield National Historic Site",
    "JELA": "Jean Lafitte National Historical Park and Preserve",
    "JECA": "Jewel Cave National Monument",
    "JICA": "Jimmy Carter National Historic Site",
    "JODA": "John Day Fossil Beds National Monument",
    "JOFI": "John Fitzgerald Kennedy National Historic Site",
    "JOMU": "John Muir National Historic Site",
    "JOFL": "Johnstown Flood National Memorial",
    "JOTR": "Joshua Tree National Park",
    "JUBA": "Juan Bautista de Anza National Historic Trail",
    "KALA": "Kalaupapa National Historical Park",
    "KAHO": "Kaloko-Honokōhau National Historical Park",
    "KAWW": "Katahdin Woods and Waters National Monument",
    "KATM": "Katmai National Park & Preserve",
    "KEFJ": "Kenai Fjords National Park",
    "KEAQ": "Kenilworth Park and Aquatic Gardens",
    "KEMO": "Kennesaw Mountain National Battlefield Park",
    "KEWE": "Keweenaw National Historical Park",
    "KIMO": "Kings Mountain National Military Park",
    "KLMN": "Klamath Network",
    "KLSE": "Klondike Gold Rush - Seattle Unit National Historical Park",
    "KLGO": "Klondike Gold Rush National Historical Park",
    "KNRI": "Knife River Indian Villages National Historic Site",
    "KOVA": "Kobuk Valley National Park",
    "KOWA": "Korean War Veterans National Memorial",
    "LACL": "Lake Clark National Park & Preserve",
    "LAKE": "Lake Mead National Recreation Area",
    "LAMR": "Lake Meredith National Recreation Area",
    "LARO": "Lake Roosevelt National Recreation Area",
    "LAVO": "Lassen Volcanic National Park",
    "LABE": "Lava Beds National Monument",
    "LECL": "Lewis and Clark National Historic Trail",
    "LEWI": "Lewis and Clark National Historical Park",
    "LIBO": "Lincoln Boyhood National Memorial",
    "LIHO": "Lincoln Home National Historic Site",
    "LINC": "Lincoln Memorial",
    "LIBI": "Little Bighorn Battlefield National Monument",
    "LIRI": "Little River Canyon National Preserve",
    "CHSC": "Little Rock Central High School National Historic Site",
    "LONG": "Longfellow House - Washington's Headquarters National Historic Site",
    "LOWE": "Lowell National Historical Park",
    "LODE": "Lower Delaware Wild and Scenic River",
    "LOEA": "Lower East Side Tenement Museum National Historic Site",
    "LYJO": "Lyndon B. Johnson National Historical Park",
    "LYBA": "Lyndon Baines Johnson Memorial Grove on the Potomac",
    "MAWA": "Maggie L. Walker National Historic Site",
    "MAAC": "Maine Acadian Culture",
    "MACA": "Mammoth Cave National Park",
    "MANA": "Manassas National Battlefield Park",
    "MAPR": "Manhattan Project National Historical Park",
    "MANZ": "Manzanar National Historic Site",
    "MABI": "Marsh-Billings-Rockefeller National Historical Park",
    "MLKM": "Martin Luther King Jr National Memorial",
    "MALU": "Martin Van Buren National Historic Site",
    "MAMC": "Mary McLeod Bethune Council House National Historic Site",
    "MTC": "Mather Training Center",
    "MEMY": "Medgar and Myrlie Evers Home National Monument",
    "MEDN": "Mediterranean Coast Network",
    "MEHI": "Meridian Hill Park",
    "MEVE": "Mesa Verde National Park",
    "MIDN": "Mid-Atlantic Network",
    "MARO": "Mid-Atlantic Regional Office",
    "MWAC": "Midwest Archeological Center",
    "MWR": "Midwest Region",
    "MWRO": "Midwest Regional Office",
    "MISP": "Mill Springs Battlefield National Monument",
    "MIIN": "Minidoka National Historic Site",
    "MIMA": "Minute Man National Historical Park",
    "MIMI": "Minuteman Missile National Historic Site",
    "MIDE": "Mississippi Delta National Heritage Area",
    "MIHI": "Mississippi Hills National Heritage Area",
    "MISS": "Mississippi National River and Recreation Areas",
    "MNRR": "Missouri National Recreational River",
    "MOJN": "Mojave Desert Network",
    "MOJA": "Mojave National Preserve",
    "MONO": "Monocacy National Battlefield",
    "MOCA": "Montezuma Castle National Monument",
    "MOCR": "Moores Creek National Battlefield",
    "MOPI": "Mormon Pioneer National Historic Trail",
    "MORR": "Morristown National Historical Park",
    "AUTO": "MotorCities National Heritage",
    "MORA": "Mount Rainier National Park",
    "MORU": "Mount Rushmore National Memorial",
    "MUWO": "Muir Woods National Monument",
    "MUSH": "Muscle Shoals National Heritage Area",
    "MRCE": "Museum Resource Center",
    "NATC": "Natchez National Historical Park",
    "NATT": "Natchez Trace National Scenic Trail",
    "NATR": "Natchez Trace Parkway",
    "AVIA": "National Aviation Heritage Area",
    "NCP": "National Capital Parks",
    "NACE": "National Capital Parks-East",
    "NCR": "National Capital Region",
    "NCRN": "National Capital Region Network",
    "COAL": "National Coal Heritage Area",
    "NAMA": "National Mall and Memorial Parks",
    "NPSA": "National Park of American Samoa",
    "NPNH": "National Parks of New York Harbor",
    "HFCA": "National Park Service History Collection",
    "NABR": "Natural Bridges National Monument",
    "NAVA": "Navajo National Monument",
    "NEBE": "New Bedford Whaling National Historical Park",
    "NEEN": "New England National Scenic Trail",
    "NEJE": "New Jersey Coastal Heritage Trail Route",
    "PINE": "New Jersey Pinelands National Reserve",
    "JAZZ": "New Orleans Jazz National Historical Park",
    "NERI": "New River Gorge National River",
    "NEPE": "Nez Perce National Historical Park",
    "NIFA": "Niagara Falls National Heritage Area",
    "NICO": "Nicodemus National Historic Site",
    "NISI": "Ninety Six National Historic Site",
    "NIOB": "Niobrara National Scenic River",
    "NOAT": "Noatak National Preserve",
    "NOCA": "North Cascades National Park",
    "NCCN": "North Coast and Cascades Network",
    "NOCO": "North Country National Scenic Trail",
    "NCBN": "Northeast Coastal and Barrier Network",
    "NER": "Northeast Region",
    "NERO": "Northeast Regional Office",
    "NETN": "Northeast Temperate Network",
    "NCPN": "Northern Colorado Plateau Network",
    "NGPN": "Northern Great Plains Network",
    "NORG": "Northern Rio Grande National Heritage Area",
    "OBED": "Obed Wild & Scenic River",
    "OCMU": "Ocmulgee Mounds National Historical Park",
    "OIRE": "Oil Region National Heritage Area",
    "OKCI": "Oklahoma City National Memorial",
    "OLSP": "Old Spanish National Historic Trail",
    "OLYM": "Olympic National Park",
    "ORCA": "Oregon Caves National Monument & Preserve",
    "OREG": "Oregon National Historic Trail",
    "ORPI": "Organ Pipe Cactus National Monument",
    "OVVI": "Overmountain Victory National Historic Trail",
    "OXHI": "Oxon Cove Park & Oxon Hill Farm",
    "OZAR": "Ozark National Scenic Riverways",
    "PACN": "Pacific Islands Network",
    "PWRO": "Pacific West Regional Office",
    "PAIS": "Padre Island National Seashore",
    "PAAL": "Palo Alto Battlefield National Historical Park",
    "PARA": "Parashant National Monument",
    "PAGR": "Paterson Great Falls National Historical Park",
    "PERI": "Pea Ridge National Military Park",
    "PECO": "Pecos National Historical Park",
    "PAAV": "Pennsylvania Avenue National Historic Site",
    "PEVI": "Perry's Victory & International Peace Memorial",
    "PETE": "Petersburg National Battlefield",
    "PEFO": "Petrified Forest National Park",
    "PETR": "Petroglyph National Monument",
    "PIRO": "Pictured Rocks National Lakeshore",
    "PINN": "Pinnacles National Park",
    "PISP": "Pipe Spring National Monument",
    "PIPE": "Pipestone National Monument",
    "PISC": "Piscataway Park",
    "PORE": "Point Reyes National Seashore",
    "POEX": "Pony Express National Historic Trail",
    "POCH": "Port Chicago Naval Magazine National Memorial",
    "POHE": "Potomac Heritage National Scenic Trail",
    "POPO": "Poverty Point National Monument",
    "WICL": "President William Jefferson Clinton Birthplace Home National Historic Site",
    "WHHO": "President's Park (White House)",
    "PRSF": "Presidio of San Francisco",
    "PRWI": "Prince William Forest Park",
    "PULL": "Pullman National Monument",
    "PUHO": "Pu'uhonua O Hōnaunau National Historical Park",
    "PUHE": "Pu'ukoholā Heiau National Historic Site",
    "QUSH": "Quinebag and Shetucket Rivers Valley",
    "RABR": "Rainbow Bridge National Monument",
    "REER": "Reconstruction Era Historical Park",
    "REDW": "Redwood National and State Parks",
    "RICH": "Richmond National Battlefield Park",
    "RIGR": "Rio Grande Wild & Scenic River",
    "RIRA": "River Raisin National Battlefield Park",
    "RIST": "Rivers of Steel National Heritage Area",
    "ROCR": "Rock Creek Park",
    "ROMO": "Rocky Mountain National Park",
    "ROMN": "Rocky Mountain Network",
    "ROWI": "Roger Williams National Memorial",
    "ROCA": "Roosevelt Campobello International Park",
    "ROVA": "Roosevelt-Vanderbilt National Historic Sites",
    "RORI": "Rosie the Riveter/World War II Home Front National Historical Park",
    "RUCA": "Russell Cave National Monument",
    "SAHI": "Sagamore Hill National Historic Site",
    "SAGU": "Saguaro National Park",
    "SACR": "Saint Croix Island International Historic Site",
    "SACN": "Saint Croix National Scenic Riverway",
    "SAPA": "Saint Paul's Church National Historic Site",
    "SAGA": "Saint-Gaudens National Historical Park",
    "SAMA": "Salem Maritime National Historic Site",
    "SAPU": "Salinas Pueblo Missions National Monument",
    "SARI": "Salt River Bay National Historical Park and Ecological Preserve",
    "SAAN": "San Antonio Missions National Historical Park",
    "SFAN": "San Francisco Bay Area Network",
    "SAFR": "San Francisco Maritime National Historical Park",
    "SAJH": "San Juan Island National Historical Park",
    "SAJU": "San Juan National Historic Site",
    "SAND": "Sand Creek Massacre National Historic Site",
    "SAMO": "Santa Monica Mountains National Recreation Area",
    "SAFE": "SantaFe National Historic Trail",
    "SARA": "Saratoga National Historical Park",
    "SAIR": "Saugus Iron Works National Historic Site",
    "SCRV": "Schuylkill River Valley National Heritage Area",
    "SCBL": "Scotts Bluff National Monument",
    "SEMO": "Selma to Montgomery National Historic Trail",
    "SEKI": "Sequoia & Kings Canyon National Parks",
    "SHEN": "Shenandoah National Park",
    "SHIL": "Shiloh National Military Park",
    "SIEN": "Sierra Nevada Netework",
    "SITK": "Sitka National Historical Park",
    "SLBE": "Sleeping Bear Dunes National Lakeshore",
    "SODN": "Sonoran Desert Network",
    "SOCA": "South Carolina National Heritage Corridor",
    "SFCN": "South Florida/Caribbean Network",
    "SEAN": "Southeast Alaska Network",
    "SEAC": "Southeast Archeological Center",
    "SECN": "Southeast Coast Network",
    "SER": "Southeast Region",
    "SERO": "Southeast Regional Office",
    "SCPN": "Southern Colorado Plateau Network",
    "SOPN": "Southern Plains Network",
    "SWAN": "Southwest Alaska Network",
    "SWAC": "Southwest Archeological Center",
    "SWR": "Southwest Region",
    "SWRO": "Southwest Regional Office",
    "SPAR": "Springfield Armory National Historic Site",
    "STSP": "Star-Spangled Banner National Historic Trail",
    "STLI": "Statue Of Liberty National Monument",
    "STGE": "Ste. Genevieve National Historical Park",
    "STEA": "Steamtown National Historic Site",
    "STRI": "Stones River National Battlefield",
    "STON": "Stonewall National Monument",
    "SUCR": "Sunset Crater Volcano National Monument",
    "TAPR": "Tallgrass Prairie National Preserve",
    "TECW": "Tennessee Civil War National Heritage Area",
    "THKO": "Thaddeus Kosciuszko National Memorial",
    "THRB": "Theodore Roosevelt Birthplace National Historic Site",
    "THRI": "Theodore Roosevelt Inaugural National Historic Site",
    "THIS": "Theodore Roosevelt Island",
    "THRO": "Theodore Roosevelt National Park",
    "THCO": "Thomas Cole National Historic Site",
    "EDIS": "Thomas Edison National Historical Park",
    "THJE": "Thomas Jefferson Memorial",
    "THST": "Thomas Stone National Historic Site",
    "TICA": "Timpanogos Cave National Monument",
    "TIMU": "Timucuan Ecological & Historic Preserve",
    "TONT": "Tonto National Monument",
    "TOSY": "Touro Synagogue National Historic Site",
    "TRTE": "Trail of Tears National Historic Trail",
    "TULE": "Tule Lake National Monument",
    "TUSK": "Tule Springs Fossil Beds National Monument",
    "TUMA": "Tumacácori National Historical Park",
    "TUPE": "Tupelo National Battlefield",
    "TUAI": "Tuskegee Airmen National Historic Site",
    "TUINT": "Tuskegee Institute National Historic Site",
    "TUZI": "Tuzigoot National Monument",
    "USPP": "U.S. Park Police",
    "ULSG": "Ulysses S. Grant National Historic Site",
    "UCBN": "Upper Columbia Basin Network",
    "UPDE": "Upper Delaware Scenic & Recreational River",
    "UPHV": "Upper Housatonic Valley National Heritage Area",
    "VALL": "Valles Caldera National Preserve",
    "VAFO": "Valley Forge National Historical Park",
    "VAMA": "Vanderbilt Mansion National Historic Site",
    "VICK": "Vicksburg National Military Park",
    "VIVE": "Vietnam Veterans Memorial",
    "VICR": "Virgin Islands Coral Reef National Monument",
    "VIIS": "Virgin Islands National Park",
    "VOYA": "Voyageurs National Park",
    "WACO": "Waco Mammoth National Monument",
    "WACA": "Walnut Canyon National Monument",
    "WAPA": "War In The Pacific National Historical Park",
    "WAMO": "Washington Monument",
    "WASO": "Washington Office",
    "WARO": "Washington-Rochambeau Revolutionary Route National Historic Trail",
    "WABA": "Washita Battlefield National Historic Site",
    "WEFA": "Weir Farm National Historic Site",
    "WACC": "Western Archeological and Conservation Center",
    "WML": "Western Museum Laboratory",
    "WRO": "Western Regional Office",
    "WHEE": "Wheeling National Heritage Area",
    "WHIS": "Whiskeytown National Recreation Area",
    "WHSA": "White Sands National Park",
    "WHMI": "Whitman Mission National Historic Site",
    "WIHO": "William Howard Taft National Historic Site",
    "WICR": "Wilson's Creek National Battlefield",
    "WICA": "Wind Cave National Park",
    "WING": "Wing Luke Museum of the Asian Pacific American Experience",
    "WOTR": "Wolf Trap National Park for the Performing Arts",
    "WORI": "Women's Rights National Historical Park",
    "WWII": "World War II Memorial National Memorial",
    "VALR": "World War II Valor in the Pacific National Monument",
    "WRST": "Wrangell - St. Elias National Park & Preserve",
    "WRBR": "Wright Brothers National Memorial",
    "WUPY": "Wupatki National Monument",
    "YELL": "Yellowstone National Park",
    "YORK": "Yorktown Battlefield",
    "YOSE": "Yosemite National Park",
    "YUHO": "Yucca House National Monument",
    "YUCH": "Yukon-Charley Rivers National Preserve",
    "YUCR": "Yuma Crossing National Heritage Area",
    "ZION": "Zion National Park"
}

baseurl = "https://17t8ywcyti.execute-api.us-east-2.amazonaws.com/test"

# 
task1_url = baseurl + "/parkboundaries/"
task2_url = baseurl + "/activitieschart"
task3_url = baseurl + "/parkimages/"

def print_park_codes():
    for code in park_map:
        print(f"{park_map[code]}: {code}")

# 
# Task 1: Park Area Computation
# 
def run_task1():
    parkcode = input("Enter a site code, or type 'list' to see all codes> ")

    if parkcode.lower() == "list":
        print_park_codes()
        parkcode = input("Enter a site code> ").strip()
    elif parkcode.upper() not in park_map:
        print("**Error: park code not found. Type 'list' to see all codes.")
        parkcode = input("Enter a site code, or type 'list' to see all codes> ")

    # api key is safe to be public since it's read-only access to public data
    url = task1_url + parkcode.lower()


    response = requests.get(url)

    if response.status_code != 200:
        print("**ERROR: failed with status code:", response.status_code)
        if response.status_code == 500:  # we'll have an error message
            body = response.json()
            print("**Message:", body["message"])

        sys.exit(0)


    body = response.json()
    print()
    print("** PARK BOUNDARIES **")
    print(f" Park Name: {body['parkname']}")
    print(f" Site Code: {body['sitecode'].upper()}")
    print(f" Area km2: {body['parkareakm']}")
    print(f" Area acres: {body['parkareaacres']}")

# 
# Task 2: activity chart generation
# 
def run_task2():
    park_input = input("Enter park codes separated by a comma and a space (i.e. yell, zion, acad) or type 'list' to see all codes> ").strip()

    if park_input.lower() == "list":
        print_park_codes()
        park_input = input("Enter park codes separated by commas> ").strip()

    park_codes = [code.strip().lower() for code in park_input.split(",") if code.strip()]

    if not park_codes:
        print("**Error: no valid park codes entered.")
        return

    payload = {
        "parkCodes": park_codes
    }

    response = requests.post(task2_url, json=payload)

    if response.status_code != 200:
        print("**ERROR: failed with status code:", response.status_code)
        try:
            outer_body = response.json()
            print("**Message:", outer_body)
        except Exception:
            print("**Raw response:", response.text)
        return

    outer_body = response.json()

    if "body" in outer_body:
        body = outer_body["body"]
        if isinstance(body, str):
            body = json.loads(body)
    else:
        body = outer_body

    print()
    print("** ACTIVITY CHART **")
    print(f" Message: {body['message']}")
    print(f" Chart URL: {body['fileUrl']}")
    print(" Park activity counts:")
    for park_name, count in body["parkCounts"].items():
        print(f"  {park_name}: {count}")


def run_task3():
    try: 
        park_input = input("Enter a park code or type 'list' to see all codes> ").strip().lower()

        while park_input == "list":
            print_park_codes()
            park_input = input("Enter park a park code or type 'list to see all codes> ").strip().lower()

        park_code = park_input.upper()

        url = task3_url + park_code 

        response = requests.get(url)

        if response.status_code != 200:
            print("**ERROR: failed with status code:", response.status_code)
            try:
                body = response.json()
                print("**Message:", body["message"])
            except Exception:
                print("**Raw response:", response.text)
            return

        body = response.json()

        print(f"**Download link for park code {park_code} is: ", body["download_link"])

        return body["download_link"]

    except Exception as err: 
        print("**Exception: ", str(err))
        raise

# 
# Main 
# 
while True:
    choice = input("Enter a task number, or type 'menu' to see options, or 'quit' to exit> ").strip().lower()

    if choice == "menu":
        print("1: Calculate Park Boundaries")
        print("2: Generate Activity Chart")
        print("3: Get Gallery Images for a Park")
        continue
    elif choice == "1":
        run_task1()
    elif choice == "2":
        run_task2()
    elif choice == "3":
        run_task3()
    elif choice == "quit":
        break
    else:
        print("**Error: invalid choice.")
