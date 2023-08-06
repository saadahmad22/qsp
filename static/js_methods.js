// from chat gpt
function convert_time_to_12_hr(americaChicagoTime) {
    // Step 1: Split the time string into hours and minutes
    const [hours, minutes] = americaChicagoTime.split(":");
  
    // Step 2: Format the time in 12-hour format with AM/PM without considering DST
    const chicagoTime = new Date();
    chicagoTime.setHours(hours, minutes, 0); // Set the time in America/Chicago timezone
  
    const localTimeOptions = {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone // Use the local timezone
    };
  
    const localTimeFormatted = chicagoTime.toLocaleString(undefined, localTimeOptions);
    return localTimeFormatted;
}

function date_sorter(a, b) {
  if (!(a && a.trim() != "--")) {
    a = "01/01/0001";
  }
  if (!(b && b.trim() != "--")) {
    b = "01/01/0001";
  }
  return new Date(a) - new Date(b);
}

function get_num_with_suffix(number) {
    // Convert the number to a string to extract the last digit
    const lastDigit = number.toString().slice(-1);
    
    // Special case for numbers ending with 11, 12, and 13
    if (number % 100 >= 11 && number % 100 <= 13) {
      return number + "th";
    }
    
    // Determine the suffix based on the last digit
    switch (lastDigit) {
      case "1":
        return number + "st";
      case "2":
        return number + "nd";
      case "3":
        return number + "rd";
      default:
        return number + "th";
    }
  }

function check_paid(row, _) {
  if (row["paid"] == "Yes" || new Date(row["pay_from_date"]) > new Date()) {
    return {
      classes : "bg-success"
    }
  }
  else if (new Date() <= new Date(row["pay_to_date"])) {
    return {
      classes : "bg-warning"
    }
  }
  return {
    classes : "bg-danger"
  }
}

// Function to set class data in the cookie
function set_class_data_in_cookie(classId, value) {
  localStorage.setItem(classId, value);
}

// Function to get class data from the cookie
function get_class_data_from_cookie(classId) {
  return localStorage.getItem(classId);
}

function get_formatted_date(date) {
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${month}${year}`;
}