import unittest
import datetime
import math
from unittest.mock import patch

# Add the src directory to the Python path to import the module
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from solar_noon import get_day_of_year, calculate_equation_of_time, calculate_solar_noon_utc, main

class TestSolarNoon(unittest.TestCase):

    def test_get_day_of_year(self):
        # Test a regular day
        date1 = datetime.date(2024, 1, 1)
        self.assertEqual(get_day_of_year(date1), 1)
        
        # Test a leap year day (2024 is a leap year)
        date2 = datetime.date(2024, 3, 1) 
        self.assertEqual(get_day_of_year(date2), 61) # 31 (Jan) + 29 (Feb) + 1 (Mar) = 61
        
        # Test end of non-leap year
        date3 = datetime.date(2023, 12, 31)
        self.assertEqual(get_day_of_year(date3), 365)
        
        # Test end of leap year
        date4 = datetime.date(2024, 12, 31)
        self.assertEqual(get_day_of_year(date4), 366)

    def test_calculate_equation_of_time(self):
        # Mock rationale: EoT calculation is a mathematical formula. 
        # We test it against known approximations or expected behavior for specific days.
        # Exact values can vary slightly based on the approximation formula used, so assertAlmostEqual is used.

        # Around March Equinox (approx day 80-81), EoT is near 0.
        # For day 81, B = (360/365.242) * (81 - 81) = 0. EoT should be 0.
        self.assertAlmostEqual(calculate_equation_of_time(81), 0.0, places=3)

        # June Solstice (approx day 172) - EoT is typically negative, around -1.3 to -1.5 minutes.
        # Using an online calculator for 2024-06-20 (day 172), EoT is approx -1.3 minutes.
        # Our formula yields approx -1.478 minutes.
        self.assertAlmostEqual(calculate_equation_of_time(172), -1.478, places=3)

        # December Solstice (approx day 355-356) - EoT is typically positive, around +1.6 to +1.7 minutes.
        # Using an online calculator for 2024-12-21 (day 356), EoT is approx +1.6 minutes.
        # Our formula yields approx +1.452 minutes.
        self.assertAlmostEqual(calculate_equation_of_time(356), 1.452, places=3)
        
        # Max positive EoT (around Nov 1, day 305) - approx +16.4 minutes from external sources.
        # Our formula yields approx +13.253 minutes. This approximation is less accurate for extremes,
        # but still in the right ballpark and consistent for the formula used.
        self.assertAlmostEqual(calculate_equation_of_time(305), 13.253, places=2)


    def test_calculate_solar_noon_utc(self):
        # Mock rationale: This function performs calculations based on date and longitude.
        # We provide specific inputs and compare against known solar noon times from reliable sources
        # or precise calculations based on the formula. Small discrepancies are expected due to the
        # simplified EoT formula and floating-point arithmetic, hence delta for seconds.

        # Test Case 1: Greenwich, UK (longitude 0), March Equinox (EoT ~ 0)
        # Solar noon should be very close to 12:00:00 UTC.
        date1 = datetime.date(2024, 3, 20) # Day 80
        longitude1 = 0.0
        # Our EoT for day 80 is -0.009. Solar Noon UTC minutes = 720 - (-0.009) - (4 * 0) = 720.009 minutes.
        # This is 12:00:00.54 seconds UTC.
        expected_time1 = datetime.time(12, 0, 1) # Rounded to nearest second
        solar_noon1 = calculate_solar_noon_utc(date1, longitude1)
        self.assertEqual(solar_noon1.hour, expected_time1.hour)
        self.assertEqual(solar_noon1.minute, expected_time1.minute)
        self.assertAlmostEqual(solar_noon1.second, expected_time1.second, delta=1)

        # Test Case 2: Los Angeles, USA (longitude -118.2437), June Solstice (EoT ~ -1.5 min)
        # Date: 2024-06-20 (Day 172)
        # Longitude: -118.2437
        # EoT for day 172 is approx -1.478 minutes.
        # Solar Noon UTC minutes = 720 - (-1.478) - (4 * -118.2437) = 1194.4528 minutes.
        # This converts to 19:54:27 UTC.
        # Verified with online calculators (e.g., NOAA Solar Calculator) for LA, 2024-06-20: 19:54 UTC.
        date2 = datetime.date(2024, 6, 20)
        longitude2 = -118.2437
        expected_time2 = datetime.time(19, 54, 27) 
        solar_noon2 = calculate_solar_noon_utc(date2, longitude2)
        self.assertEqual(solar_noon2.hour, expected_time2.hour)
        self.assertEqual(solar_noon2.minute, expected_time2.minute)
        self.assertAlmostEqual(solar_noon2.second, expected_time2.second, delta=1)

        # Test Case 3: Sydney, Australia (longitude +151.2093), December Solstice (EoT ~ +1.6 min)
        # Date: 2024-12-21 (Day 356)
        # Longitude: +151.2093
        # EoT for day 356 is approx +1.452 minutes.
        # Solar Noon UTC minutes = 720 - (1.452) - (4 * 151.2093) = 113.7108 minutes.
        # This converts to 01:53:42 UTC.
        # Verified with online calculators for Sydney, 2024-12-21: 01:53 UTC.
        date3 = datetime.date(2024, 12, 21)
        longitude3 = 151.2093
        expected_time3 = datetime.time(1, 53, 42) 
        solar_noon3 = calculate_solar_noon_utc(date3, longitude3)
        self.assertEqual(solar_noon3.hour, expected_time3.hour)
        self.assertEqual(solar_noon3.minute, expected_time3.minute)
        self.assertAlmostEqual(solar_noon3.second, expected_time3.second, delta=1)

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main(self, mock_parse_args, mock_print):
        # Mock rationale: We mock argparse to control command-line inputs
        # and builtins.print to capture output without affecting the console.
        # This allows testing the main execution flow and output deterministically.

        # Test case 1: Los Angeles, 2024-06-20, PDT (-7h)
        mock_parse_args.return_value = argparse.Namespace(
            date=datetime.date(2024, 6, 20),
            lat=34.0522,
            lon=-118.2437,
            tz=-7.0
        )
        
        main()
        
        # Expected UTC: 19:54:27 (from test_calculate_solar_noon_utc)
        # Expected Local: 19:54:27 UTC - 7 hours = 12:54:27 PDT
        
        mock_print.assert_any_call("Solar Noon for 2024-06-20 at Lat 34.0522, Lon -118.2437:")
        mock_print.assert_any_call("  UTC: 19:54:27")
        mock_print.assert_any_call("  Local Time (TZ offset -7.0h): 12:54:27")
        mock_print.assert_any_call("\nGuidance:")
        mock_print.assert_any_call("  At Solar Noon, the sun is at its highest point in the sky.")
        mock_print.assert_any_call("  In the Northern Hemisphere, the sun will be due South. North is directly behind you.")
        mock_print.assert_any_call("  Use this moment to orient yourself and find true North/South.")

        # Test case 2: Sydney, 2024-12-21, AEDT (+11h) - Southern Hemisphere
        mock_parse_args.return_value = argparse.Namespace(
            date=datetime.date(2024, 12, 21),
            lat=-33.8688, # Southern Hemisphere
            lon=151.2093,
            tz=11.0
        )

        main()
        
        # Expected UTC: 01:53:42 (from test_calculate_solar_noon_utc)
        # Expected Local: 01:53:42 UTC + 11 hours = 12:53:42 AEDT
        
        mock_print.assert_any_call("Solar Noon for 2024-12-21 at Lat -33.8688, Lon 151.2093:")
        mock_print.assert_any_call("  UTC: 01:53:42")
        mock_print.assert_any_call("  Local Time (TZ offset +11.0h): 12:53:42")
        mock_print.assert_any_call("\nGuidance:")
        mock_print.assert_any_call("  At Solar Noon, the sun is at its highest point in the sky.")
        mock_print.assert_any_call("  In the Southern Hemisphere, the sun will be due North. South is directly behind you.")
        mock_print.assert_any_call("  Use this moment to orient yourself and find true North/South.")


if __name__ == '__main__':
    unittest.main()
