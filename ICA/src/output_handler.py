import logging
from datetime import datetime, date, timedelta
from models.city import City
from models.country import Country
from models.daily_weather_entry import DailyWeatherEntry
from output_handler_registry import OutputHandlerRegistry
from sqlalchemy.engine.row import Row
from constants import *

class OutputHandler:
    """
    Provides methods to display results in the console.
    """
    logger = logging.getLogger(__name__)

    @staticmethod
    def handle_output(choice, results, title=None, xlabel=None, ylabel=None):
        """
        Delegates output handling based on the user's choice.
        Parameters
        ----------
        choice : int
            The display choice (i.e., 1 for console, 2 for bar chart, etc.).
        results : list of dictionaries or single values 
            The data to display.
        title : str, optional
            The title for graphical outputs.
        xlabel : str, optional
            The x-axis label for graphical outputs.
        ylabel : str, optional
            The y-axis label for graphical outputs.
        """
        OutputHandler.logger.debug("handle_output called with choice=%s, title=%s", choice, title)
        OutputHandler.logger.debug("Raw results (before standardise): %r", results)

        if not results:
            print("No data available.")
            OutputHandler.logger.warning("No data available.")
            return

        results = OutputHandler._standardise_results(results, title)
        OutputHandler.logger.debug("Results after _standardise_results: type=%s, value=%r", type(results), results)

        if not isinstance(results, list):
            OutputHandler.logger.debug("Results is not a list; falling back to console output.")
            print("Results should be a list or a numeric value. Falling back to console.")
            OutputHandler._display_table(results)
            return

        ### ADDED LOGGING ###
        OutputHandler.logger.debug("About to extract labels/values from results.")
        labels, values = OutputHandler._extract_labels_values_for_cities_and_countries(results)
        OutputHandler.logger.debug("After _extract_labels_values_for_cities_and_countries:")
        OutputHandler.logger.debug("   labels=%r", labels)
        OutputHandler.logger.debug("   values=%r", values)

        handlers = {
            1: "console",
            2: "bar_chart",
            3: "pie_chart"
        }
        handler_name = handlers.get(choice)
        handler = OutputHandlerRegistry.get_handler(handler_name)

        try:
            if handler_name == "console":
                OutputHandler.logger.debug("User chose console output.")
                OutputHandler._display_table(results)
            elif handler:
                OutputHandler.logger.debug("User chose graph output. Handler=%s", handler_name)
                OutputHandler.logger.debug("Graphing with labels: %r and values: %r", labels, values)
                handler(choice, labels, values, title, xlabel, ylabel)
            else:
                raise ValueError(f"Unsupported output type: {handler_name}")
        except Exception as e:
            OutputHandler.logger.error(
                "Error during output handling. Handler: %s, Choice: %s, Error: %s",
                handler_name, choice, e, exc_info=True
            )
            print(f"Error: Unable to generate chart. {e}")
            print("Falling back to console output.")
            OutputHandler._display_table(results)

    @staticmethod
    def _extract_labels_values_for_cities_and_countries(results):
        """
        Extract labels and values for graphs.
        Parameters
        ----------
        results : list[dict]
            Query results as a list of dictionaries.
        Returns
        -------
        tuple[list, list]
            A tuple containing labels (x-axis) and values (y-axis) for charts.
        """
        ### ADDED LOGGING ###
        OutputHandler.logger.debug("_extract_labels_values_for_cities_and_countries called.")
        OutputHandler.logger.debug("Incoming results type=%s, length=%d", type(results), len(results) if results else 0)

        # Handle empty results
        if not results or not isinstance(results[0], dict):
            OutputHandler.logger.debug("results is empty or results[0] is not a dict. Returning fallback.")
            return ["No data"], [0]
        
        # 1) If we have daily precipitation data
        if 'date' in results[0] and 'precipitation' in results[0]:
            OutputHandler.logger.debug("Detected 'date' and 'precipitation' in results[0], daily data path.")
            labels = [str(row['date']) for row in results]
            values = [row['precipitation'] for row in results]
            return labels, values

        # 2) Start with empty defaults
        labels = []
        values = []

        # 3) If monthly data
        if "Month" in results[0]:
            OutputHandler.logger.debug("Detected 'Month' in results[0], monthly data path.")
            values = [row["Temperature"] for row in results]
            labels = OutputHandler._generate_time_period_labels(results)
            OutputHandler.logger.debug("Monthly data assigned labels=%r, values=%r", labels, values)

        # 4) If STILL empty, fallback to generic approach
        if not labels:
            OutputHandler.logger.debug("labels is empty. Generating fallback labels from dict keys.")
            labels = list(results[0].keys())
        if not values:
            OutputHandler.logger.debug("values is empty. Generating fallback values from each row's values.")
            values = [list(row.values()) for row in results]

        OutputHandler.logger.debug("Returning from _extract_labels_values_for_cities_and_countries with:")
        OutputHandler.logger.debug("   labels=%r", labels)
        OutputHandler.logger.debug("   values=%r", values)
        return labels, values

    @staticmethod
    def _standardise_results(results, title):
        """
        Standardize results to a list format and format numeric values to 2 decimal places.
        """
        OutputHandler.logger.debug("_standardise_results called, title=%s", title)
        OutputHandler.logger.debug("Type of incoming results: %s", type(results))

        # If results is a numeric type (int or float), return it as a formatted dictionary
        if isinstance(results, (int, float)):
            OutputHandler.logger.debug("results is numeric; returning single dict with 'Result'.")
            return [{"Result": f"{results:.2f}"}]

        # If results is a dictionary, process it as such
        if isinstance(results, dict):
            OutputHandler.logger.debug("results is a dict; checking for specific titles.")
            if 'Average Seven-Day Precipitation' == title:
                total_precip = results.get('total_precipitation', 0)
                results['total_precipitation'] = round(total_precip, 2)

            if 'Average Temperature' == title:
                OutputHandler.logger.debug("'Average Temperature' in title, converting month->list[dict].")
                standardized_results = [
                    {"Month": month, "Temperature": f"{temp:.2f}"}
                    for month, temp in results.items()
                ]
                return standardized_results

            if 'Mean Temperature by City' == title:
                total_precip = results.get('total_precipitation', 0)
                results['total_precipitation'] = round(total_precip, 2)
            return results

        # If results is a list
        if isinstance(results, list):
            OutputHandler.logger.debug("results is a list; may contain tuples, DailyWeatherEntry, City, or dict.")
            standardised = []
            for row in results:
                # 1) If it's a tuple
                if isinstance(row, tuple):
                    OutputHandler.logger.debug(f"Row is a tuple: {row}")
                    standardised.append({'precipitation': round(row[0], 2)})

                # 2) If it's a DailyWeatherEntry
                elif isinstance(row, DailyWeatherEntry):
                    OutputHandler.logger.debug(f"Row is a DailyWeatherEntry: {row}")
                    standardised.append({
                        'date': row.date,
                        'precipitation': float(row.precipitation),
                        'max_temp': float(row.max_temp),
                        'min_temp': float(row.min_temp),
                    })

                # 3) If it's City or Country
                elif isinstance(row, (City, Country)):
                    OutputHandler.logger.debug(f"Row is a City/Country: {row}")
                    if hasattr(row, 'to_dict'):
                        standardised.append(row.to_dict())
                    else:
                        OutputHandler.logger.debug("No to_dict method found for row.")
                # 4) If it's already a dict
                elif isinstance(row, dict):
                    OutputHandler.logger.debug("Row is already a dict: %r", row)
                    standardised.append(row)

            OutputHandler.logger.debug("Returning standardised list of length %d.", len(standardised))
            return standardised

        # If results is neither numeric nor dict/list, return empty list
        OutputHandler.logger.debug("results is neither numeric nor dict/list; returning [].")
        return []

    @staticmethod
    def _display_table(results):
        """
        Display results in tabular format, ensuring numeric values are formatted to 2 decimal places.
        Parameters
        ----------
        results : list[dict]
            The tabular results to display.
        """
        OutputHandler.logger.debug("_display_table called.")
        if not results or not isinstance(results, list):
            print()
            print("No data to display.")
            return

        if 'Temperature' in results[0]:
            OutputHandler.logger.debug("Detected 'Temperature' key in first row; calling _display_temperature_table.")
            OutputHandler._display_temperature_table(results)
        elif 'precipitation' in results[0]:
            OutputHandler.logger.debug("Detected 'precipitation' key in first row; calling _display_precipitation_table.")
            OutputHandler._display_precipitation_table(results)
        else:
            OutputHandler.logger.debug("Generic data, calling _print_to_console.")
            OutputHandler._print_to_console(results)

    @staticmethod
    def _print_to_console(results):
        OutputHandler.logger.debug("_print_to_console called.")
        if not results:
            print("No data to display.")
            return
        headers = list(results[0].keys())
        column_widths = {header: len(header) for header in headers}

        for row in results:
            for header in headers:
                value = row.get(header, "")
                if header in {"id", "country_id"} and value is not None:
                    try:
                        value = int(float(value))
                    except ValueError:
                        pass
                if isinstance(value, (int, float)) and header not in {"latitude", "longitude"}:
                    value = round(value, 2)
                    value = f"{value:.2f}"
                column_widths[header] = max(column_widths[header], len(str(value)))

        header_format = " | ".join(f"{{:<{column_widths[header]}}}" for header in headers)
        separator = "-+-".join("-" * column_widths[header] for header in headers)

        print()
        print(header_format.format(*headers))
        print(separator)

        for row in results:
            row_values = [
                str(int(row.get(header, 0))) if header in {"id", "country_id"} and row.get(header) is not None
                else str(row.get(header, "N/A"))
                for header in headers
            ]
            print(header_format.format(*row_values))

    @staticmethod
    def _display_temperature_table(results):
        OutputHandler.logger.debug("_display_temperature_table called.")
        if not results:
            OutputHandler.logger.info("No temperature data available.")
            return
        headers = ['Month', 'Temperature °C']
        column_widths = {header: len(header) for header in headers}
        column_widths['Month'] = max(len(month) for month in MONTH_NAMES)

        for item in results:
            temperature = item.get("Temperature")
            if temperature is not None:
                column_widths['Temperature °C'] = max(
                    column_widths['Temperature °C'], len(f"{float(temperature):.2f}")
                )

        header_line = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
        separator = "-+-".join("-" * column_widths[header] for header in headers)
        print()
        print(header_line)
        print(separator)

        for item in results:
            month = item.get("Month")
            temperature = item.get("Temperature")
            if month is not None and temperature is not None:
                try:
                    temperature = float(temperature)
                    month_name = MONTH_NAMES[month - 1]
                    print(f"{month_name:<{column_widths['Month']}} | {temperature:<{column_widths['Temperature °C']}.2f}")
                except ValueError:
                    OutputHandler.logger.error("Invalid temperature value: %r", temperature)
                    print(f"{month_name:<{column_widths['Month']}} | Invalid Temperature")
            else:
                OutputHandler.logger.error("Missing Month or Temperature in item: %r", item)
                print(f"{'Invalid Data':<{column_widths['Month']}} | {'Invalid Data':<{column_widths['Temperature °C']}}")

    @staticmethod
    def _display_precipitation_table(results):
        OutputHandler.logger.debug("_display_precipitation_table called.")
        if not results:
            OutputHandler.logger.info("No precipitation data available.")
            return
        headers = ['ID', 'Date', 'Precipitation']
        column_widths = {header: len(header) for header in headers}

        for row in results:
            for header in headers:
                value = row.get(header.lower(), '')
                column_widths[header] = max(column_widths[header], len(str(value)))

        header_line = " | ".join(f"{header:<{column_widths[header]}}" for header in headers)
        separator = "-+-".join("-" * column_widths[header] for header in headers)
        print()
        print(header_line)
        print(separator)

        for row in results:
            print(" | ".join(f"{str(row.get(header.lower(), '')):<{column_widths[header]}}" for header in headers))

    @staticmethod
    def handle_console(results):
        OutputHandler.logger.debug("handle_console called.")
        if isinstance(results, (int, float)):
            print(f"Experiencing {results:.2f} mm of precipitation")
            return
        if not results or not isinstance(results, list) or not isinstance(results[0], dict):
            print("No valid data available.")
            return
        headers = results[0].keys()
        header_line = " | ".join(headers)
        print(f"Header Line: {header_line}")
        print("-" * len(header_line))

        for result in results:
            row_line = " | ".join(str(result.get(key, "N/A")) for key in headers)
            print(row_line)

    @staticmethod
    def sqlite_row_to_dict(rows):
        OutputHandler.logger.debug("sqlite_row_to_dict called.")
        return [dict(row) for row in rows]

    @staticmethod
    def _generate_time_period_labels(results):
        import logging
        logger = logging.getLogger(__name__)

        logger.debug("_generate_time_period_labels called. Checking if 'Month' in results[0].")
        if "Month" in results[0]:
            labels = [MONTH_NAMES[row["Month"] - 1] for row in results if "Month" in row]
            logger.debug("Generated month-based labels: %r", labels)
            return labels

        logger.debug("No 'Month' found; proceeding with daily or multi-month logic.")
        start_date = datetime.strptime(results[0]['date'], '%Y-%m-%d')
        end_date = datetime.strptime(results[-1]['date'], '%Y-%m-%d')
        days_difference = (end_date - start_date).days + 1
        logger.debug(f"Days difference: {days_difference}")

        labels = []

        if days_difference <= 14:
            logger.debug("Generating daily labels.")
            for i in range(days_difference):
                label_date = start_date + timedelta(days=i)
                labels.append(label_date.strftime('%Y-%m-%d'))
        elif days_difference <= 31:
            logger.debug("Generating labels every 2 days (15-31 days).")
            for i in range(0, days_difference, 2):
                label_date = start_date + timedelta(days=i)
                labels.append(label_date.strftime('%Y-%m-%d'))
        else:
            months_difference = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
            logger.debug(f"Months difference: {months_difference}")
            if months_difference <= 12:
                logger.debug("Generating monthly labels (<=12 months).")
                for i in range(months_difference):
                    month_label = (start_date + timedelta(days=30 * i)).strftime('%b %Y')
                    labels.append(month_label)
            elif months_difference <= 24:
                logger.debug("Generating quarterly labels (<=24 months).")
                for i in range(0, months_difference, 3):
                    quarter_label = f"Q{(i // 3) + 1} ({start_date.year + (i // 12)})"
                    labels.append(quarter_label)
            elif months_difference <= 48:
                logger.debug("Generating half-yearly labels (<=48 months).")
                for i in range(0, months_difference, 6):
                    half_year_label = f"H{(i // 6) + 1} ({start_date.year + (i // 12)})"
                    labels.append(half_year_label)
            else:
                logger.debug("Generating yearly labels (>48 months).")
                for i in range(0, months_difference, 12):
                    year_label = f"{start_date.year + (i // 12)}"
                    labels.append(year_label)

        logger.debug("Time period labels generated: %r", labels)
        logger.debug("Label count: %d", len(labels))
        return labels
