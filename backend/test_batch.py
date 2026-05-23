import requests

API = "http://localhost:8000/predict"

# Helper to build a full payload with sensible defaults
def case(name, expected, **kw):
    defaults = {
        "weather_condition": "CLEAR",
        "lighting_condition": "DAYLIGHT",
        "roadway_surface_cond": "DRY",
        "road_defect": "NO DEFECTS",
        "traffic_control_device": "TRAFFIC SIGNAL",
        "trafficway_type": "NOT DIVIDED",
        "alignment": "STRAIGHT AND LEVEL",
        "intersection_related_i": "N",
        "first_crash_type": "REAR END",
        "prim_contributory_cause": "FAILING TO YIELD RIGHT-OF-WAY",
        "damage": "OVER $1,500",
        "num_units": 2,
        "crash_hour": 12,
        "crash_day_of_week": 3,
        "crash_month": 6,
    }
    defaults.update(kw)
    return {"name": name, "expected": expected, "payload": defaults}

tests = [
    case("1. Clear Safe Driving",      "NO_INJURY",
         trafficway_type="ONE-WAY", crash_hour=11, crash_day_of_week=2, crash_month=6),

    case("2. Rainy Night",             "MINOR",
         weather_condition="RAIN", lighting_condition="DARKNESS",
         roadway_surface_cond="WET", traffic_control_device="STOP SIGN/FLASHER",
         trafficway_type="NOT DIVIDED", intersection_related_i="Y",
         crash_hour=22, crash_day_of_week=6, crash_month=11,
         first_crash_type="ANGLE", prim_contributory_cause="FAILING TO REDUCE SPEED"),

    case("3. Heavy Snow Highway",      "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="SNOW OR SLUSH", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=2, crash_day_of_week=7, crash_month=1,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("4. Foggy Morning",           "MINOR",
         weather_condition="FOG/SMOKE/HAZE", lighting_condition="DAWN",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER", intersection_related_i="Y",
         crash_hour=7, crash_day_of_week=1, crash_month=10,
         first_crash_type="TURNING", prim_contributory_cause="VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)"),

    case("5. Late Night Icy Curve",    "SEVERE",
         weather_condition="FREEZING RAIN/DRIZZLE", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON HILLCREST", crash_hour=1, crash_day_of_week=5, crash_month=12,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("6. Sunny Afternoon",         "NO_INJURY",
         trafficway_type="ONE-WAY", crash_hour=15, crash_day_of_week=3, crash_month=4),

    case("7. Wet Intersection Night",  "MINOR",
         weather_condition="RAIN", lighting_condition="DARKNESS, LIGHTED ROAD",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="NOT DIVIDED", intersection_related_i="Y",
         crash_hour=21, crash_day_of_week=6, crash_month=9,
         first_crash_type="ANGLE", prim_contributory_cause="FAILING TO YIELD RIGHT-OF-WAY"),

    case("8. Dangerous Rural Curve",   "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=3, crash_day_of_week=7, crash_month=1,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("9. Daylight Urban Traffic",  "NO_INJURY",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER", intersection_related_i="Y",
         crash_hour=13, crash_day_of_week=4, crash_month=5),

    case("10. Thunderstorm Highway",   "SEVERE",
         weather_condition="RAIN", lighting_condition="DARKNESS",
         roadway_surface_cond="WET", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=0, crash_day_of_week=6, crash_month=8,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),
             case("11. Clear Residential Morning", "NO_INJURY",
         trafficway_type="ONE-WAY", crash_hour=9, crash_day_of_week=1, crash_month=3),

    case("12. Rainy Downtown Rush",      "MINOR",
         weather_condition="RAIN", lighting_condition="DUSK",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER", intersection_related_i="Y",
         crash_hour=18, crash_day_of_week=5, crash_month=9,
         first_crash_type="REAR END", prim_contributory_cause="FOLLOWING TOO CLOSELY"),

    case("13. Snowy Freeway Curve",      "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="SNOW OR SLUSH", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=2, crash_day_of_week=6, crash_month=1,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("14. Foggy School Zone",        "MINOR",
         weather_condition="FOG/SMOKE/HAZE", lighting_condition="DAYLIGHT",
         roadway_surface_cond="DAMP", traffic_control_device="STOP SIGN/FLASHER",
         trafficway_type="ONE-WAY", intersection_related_i="Y",
         crash_hour=8, crash_day_of_week=2, crash_month=10,
         first_crash_type="SIDESWIPE SAME DIRECTION",
         prim_contributory_cause="IMPROPER OVERTAKING/PASSING"),

    case("15. Midnight Ice Road",        "SEVERE",
         weather_condition="FREEZING RAIN/DRIZZLE", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON HILLCREST", crash_hour=1, crash_day_of_week=7, crash_month=12,
         first_crash_type="FIXED OBJECT", prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("16. Sunny Highway Cruise",     "NO_INJURY",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER",
         crash_hour=14, crash_day_of_week=4, crash_month=5),

    case("17. Wet Night Junction",       "MINOR",
         weather_condition="RAIN", lighting_condition="DARKNESS, LIGHTED ROAD",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="NOT DIVIDED", intersection_related_i="Y",
         crash_hour=22, crash_day_of_week=6, crash_month=8,
         first_crash_type="ANGLE",
         prim_contributory_cause="DISREGARDING TRAFFIC SIGNALS"),

    case("18. Rural Blizzard Crash",     "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=4, crash_day_of_week=7, crash_month=2,
         first_crash_type="OVERTURNED",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("19. Downtown Noon Traffic",    "NO_INJURY",
         trafficway_type="ONE-WAY", intersection_related_i="Y",
         crash_hour=12, crash_day_of_week=3, crash_month=6),

    case("20. Heavy Rain Exit Ramp",     "SEVERE",
         weather_condition="RAIN", lighting_condition="DARKNESS",
         roadway_surface_cond="WET", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON HILLCREST", crash_hour=0, crash_day_of_week=5, crash_month=9,
         first_crash_type="FIXED OBJECT",
         prim_contributory_cause="FAILING TO REDUCE SPEED",
         damage="OVER $1,500", num_units=1),

    case("21. Dry Afternoon Suburb",     "NO_INJURY",
         trafficway_type="ONE-WAY",
         crash_hour=15, crash_day_of_week=2, crash_month=4),

    case("22. Rainy Dawn Commute",       "MINOR",
         weather_condition="RAIN", lighting_condition="DAWN",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER", intersection_related_i="Y",
         crash_hour=7, crash_day_of_week=1, crash_month=11,
         first_crash_type="REAR END",
         prim_contributory_cause="FOLLOWING TOO CLOSELY"),

    case("23. Snow Covered Highway",     "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="SNOW OR SLUSH", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE", crash_hour=3, crash_day_of_week=6, crash_month=1,
         first_crash_type="FIXED OBJECT",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("24. Foggy Bridge Crossing",    "MINOR",
         weather_condition="FOG/SMOKE/HAZE", lighting_condition="DAWN",
         roadway_surface_cond="DAMP", traffic_control_device="STOP SIGN/FLASHER",
         trafficway_type="NOT DIVIDED", intersection_related_i="Y",
         crash_hour=6, crash_day_of_week=4, crash_month=10,
         first_crash_type="ANGLE",
         prim_contributory_cause="UNABLE TO DETERMINE"),

    case("25. Sunny Open Freeway",       "NO_INJURY",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER",
         crash_hour=16, crash_day_of_week=5, crash_month=7),

    case("26. Wet Evening Curve",        "MINOR",
         weather_condition="RAIN", lighting_condition="DUSK",
         roadway_surface_cond="WET", traffic_control_device="YIELD",
         trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE",
         crash_hour=19, crash_day_of_week=6, crash_month=9,
         first_crash_type="SIDESWIPE OPPOSITE DIRECTION",
         prim_contributory_cause="IMPROPER LANE USAGE"),

    case("27. Ice Storm Rural Road",     "SEVERE",
         weather_condition="FREEZING RAIN/DRIZZLE", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON HILLCREST",
         crash_hour=2, crash_day_of_week=7, crash_month=2,
         first_crash_type="OVERTURNED",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("28. Calm Urban Noon",          "NO_INJURY",
         trafficway_type="ONE-WAY", intersection_related_i="Y",
         crash_hour=11, crash_day_of_week=2, crash_month=5),

    case("29. Rainy Traffic Jam",        "MINOR",
         weather_condition="RAIN", lighting_condition="DAYLIGHT",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER", intersection_related_i="Y",
         crash_hour=17, crash_day_of_week=5, crash_month=8,
         first_crash_type="REAR END",
         prim_contributory_cause="FOLLOWING TOO CLOSELY"),

    case("30. Snowy Mountain Curve",     "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="SNOW OR SLUSH", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE",
         crash_hour=1, crash_day_of_week=6, crash_month=12,
         first_crash_type="FIXED OBJECT",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("31. Bright Summer Drive",      "NO_INJURY",
         trafficway_type="ONE-WAY",
         crash_hour=13, crash_day_of_week=3, crash_month=7),

    case("32. Foggy Rural Morning",      "MINOR",
         weather_condition="FOG/SMOKE/HAZE", lighting_condition="DAWN",
         roadway_surface_cond="DAMP", traffic_control_device="STOP SIGN/FLASHER",
         trafficway_type="NOT DIVIDED", intersection_related_i="Y",
         crash_hour=7, crash_day_of_week=1, crash_month=11,
         first_crash_type="ANGLE",
         prim_contributory_cause="VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)"),

    case("33. Slippery Night Highway",   "SEVERE",
         weather_condition="FREEZING RAIN/DRIZZLE", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE",
         crash_hour=0, crash_day_of_week=7, crash_month=1,
         first_crash_type="FIXED OBJECT",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("34. Downtown Afternoon",       "NO_INJURY",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER",
         intersection_related_i="Y",
         crash_hour=14, crash_day_of_week=4, crash_month=6),

    case("35. Wet Rush Hour",            "MINOR",
         weather_condition="RAIN", lighting_condition="DUSK",
         roadway_surface_cond="WET", traffic_control_device="TRAFFIC SIGNAL",
         trafficway_type="ONE-WAY", intersection_related_i="Y",
         crash_hour=18, crash_day_of_week=5, crash_month=9,
         first_crash_type="REAR END",
         prim_contributory_cause="FOLLOWING TOO CLOSELY"),

    case("36. Dangerous Ice Curve",      "SEVERE",
         weather_condition="FREEZING RAIN/DRIZZLE", lighting_condition="DARKNESS",
         roadway_surface_cond="ICE", road_defect="RUT, HOLES",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON HILLCREST",
         crash_hour=2, crash_day_of_week=6, crash_month=2,
         first_crash_type="OVERTURNED",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("37. Dry Residential Noon",     "NO_INJURY",
         trafficway_type="ONE-WAY",
         crash_hour=12, crash_day_of_week=2, crash_month=5),

    case("38. Rainy Highway Merge",      "MINOR",
         weather_condition="RAIN", lighting_condition="DARKNESS, LIGHTED ROAD",
         roadway_surface_cond="WET", traffic_control_device="YIELD",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER",
         crash_hour=20, crash_day_of_week=5, crash_month=10,
         first_crash_type="SIDESWIPE SAME DIRECTION",
         prim_contributory_cause="IMPROPER LANE USAGE"),

    case("39. Blizzard Night Crash",     "SEVERE",
         weather_condition="SNOW", lighting_condition="DARKNESS",
         roadway_surface_cond="SNOW OR SLUSH", road_defect="OTHER",
         traffic_control_device="NO CONTROLS", trafficway_type="NOT DIVIDED",
         alignment="CURVE ON GRADE",
         crash_hour=1, crash_day_of_week=7, crash_month=1,
         first_crash_type="FIXED OBJECT",
         prim_contributory_cause="WEATHER",
         damage="OVER $1,500", num_units=1),

    case("40. Sunny Weekend Drive",      "NO_INJURY",
         trafficway_type="DIVIDED - W/MEDIAN BARRIER",
         crash_hour=16, crash_day_of_week=6, crash_month=6),
]

passed = failed = 0

print(f"\n{'='*60}")
print(f"  BATCH TEST — {len(tests)} cases")
print(f"{'='*60}\n")

for t in tests:
    try:
        r = requests.post(API, json=t["payload"], timeout=5)
        r.raise_for_status()
        got = r.json().get("predicted_severity", "N/A")
        conf = r.json().get("confidence", {})
        ok = got == t["expected"]
        status = "PASS ✓" if ok else "FAIL ✗"
        passed += ok; failed += not ok
        print(f"[{status}]  {t['name']}")
        if not ok:
            print(f"         expected: {t['expected']}  |  got: {got}")
        conf_str = "  ".join(f"{k}: {v}%" for k, v in conf.items())
        print(f"         {conf_str}")
    except Exception as e:
        failed += 1
        print(f"[ERROR]  {t['name']}  →  {e}")

print(f"\n{'='*60}")
print(f"  Results: {passed} passed, {failed} failed out of {len(tests)}")
print(f"{'='*60}\n")
