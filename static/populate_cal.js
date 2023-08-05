function create_cal() {
    populate_info();
    populate_cal();
}

function populate_cal_info(date) {
    if (!$.trim($("#calendar_extra_info_header").html())) {
        $("#calendar_extra_info_header").html(`Notes about class on the ${get_num_with_suffix(date)}`);
        $("#calendar_extra_info").html(`${calendar_json.month[date].notes}`);
    }
    else {
        empty_header();
    }
}

function new_month(month_id) {
    empty_header();
    $("#calendar").empty()

    if (month_id != undefined) {
        fetch_cal(month_id);
        set_class_data_in_cookie(calendar_json.schedule_id, calendar_json.month.id);
    }
    else {
        fetch_cal();
        if (today_in_cal()) {
            new_month(get_formatted_date(new Date()));
        }
    }
    create_cal();
}

function today_in_cal() {
    return calendar_json.months.includes(get_formatted_date(new Date()));
}

function empty_header() {
    $("#calendar_extra_info_header").empty()
    $("#calendar_extra_info").empty()
}

function populate_id(id, json_data, selected_val) {
    selected_element = document.getElementById(id);
    new_html = selected_val == -1 ? '<option disabled selected="true" value="-1"> Select class</option>' : 
        '<option disabled value="-1"> Select class</option>';
    // Credit to below code to James Hibbard on sitepoint.com
    Object.entries(json_data).forEach((schedule) => {
        const [id, data_] = schedule;
        if (selected_val == id) {
            new_html += `<option selected disabled value=${id}>${data_.title} with ${data_.first} ${data_.last}</option>`
        }
        else {
            new_html += `<option value=${id}>${data_.title} with ${data_.first} ${data_.last}</option>`
        }
    });
    selected_element.innerHTML = new_html;
} 

function populate_info() {
    if (calendar_json == null) {
        error_template(
            {"responseText" : "Header information not found"},
            404,
            "Information not found"
            );
    }
        
    $("#calendar_info").html('<h5 class="card-title" style="text-align: start;">Class Schedule</h5>');
    $("#calendar_info").append(`<p class="card-text" style="text-align: start;">${calendar_json.title} with ${calendar_json.name}</p>`);
    $("#calendar_info").append(`<small class="card-text" style="display: flex">${calendar_json.desc}</small></br>`);
    let days_info = '<ul class="list-group" style="max-width:30%">' +  
        '<li> <h6 class="list-group-item list-group-item-action active">Class Days</h6> </li>';
        calendar_json.generic_days.forEach((day) => {
                weekday = day.weekday;
                days_info += `
                <li style="width:100%;text-align:start">${weekday.name} : ${convert_time_to_12_hr(weekday.start)} - ${convert_time_to_12_hr(weekday.end)}</li>`;
            });
    $("#calendar_info").append(`${days_info}
    </ul>`);
    if (calendar_json.digital_meeting_link != undefined && calendar_json.digital_meeting_link != "None" && calendar_json.digital_meeting_link.length > 1) {
        $("#calendar_info").append(`<a class="card-text" style="display: flex" href="Class Meeting Link : ${calendar_json.digital_meeting_link}">${calendar_json.digital_meeting_link}</a>`);
    }

}

function populate_cal() {
    let calendarHTML = `
        <div id="row1" class="cal_row inline_row">
            <div id="left_portion" class="cal_row">
            <h1>${calendar_json.month.name}, ${calendar_json.month.year}</h1>
            </div>
            <div id="right_portion" >`;
            if (calendar_json.month.prev.is_class) {
                calendarHTML += `<button class="cal_button today_button" onclick="new_month('${calendar_json.month.prev.id.toString()}')">&#60;</button>`;
            }
            else {
                calendarHTML += `<button disabled class="cal_button today_button")">&#60;</button>`;
            }
            calendarHTML += "";
            if (today_in_cal()) {
                calendarHTML += `<button class="cal_button today_button" onclick="new_month('${get_formatted_date(new Date())}')">Today</button>`;
            }
            if (calendar_json.month.next.is_class) {
                calendarHTML += `<button class="cal_button today_button" onclick="new_month('${calendar_json.month.next.id.toString()}')">&#62;</button>`;
            }
            else {
                calendarHTML += `<button disabled class="cal_button today_button")">&#62;</button>`;
            }

    calendarHTML += `
            </div>
        </div>
        <table class="date_container">
            <thead>
                <tr class="cal_row">
                    <th class="cal_cell">Sun</th>
                    <th class="cal_cell">Mon</th>
                    <th class="cal_cell">Tue</th>
                    <th class="cal_cell">Wed</th>
                    <th class="cal_cell">Thu</th>
                    <th class="cal_cell">Fri</th>
                    <th class="cal_cell">Sat</th>
                </tr>
            </thead>
            <tbody style="background-color: seashell;">
    `;
    const first_day = (calendar_json.month.first_day + 1) % 7;
    let date = 0;
    
    for (let row = 0; row < calendar_json.month.weeks; row++) {
      calendarHTML += '<tr class="cal_row">';
      for (let day = 0; day < 7; day++) {
        if ((row === 0 && (day < first_day || (day === 0 && first_day === 0))) || date >= calendar_json.month.last_day) {
          calendarHTML += `
            <td class="cal_cell">
              <span class="day" id="0">&nbsp;</span>
            </td>
          `;
        } else {
          date++;
          // Add top
          if (today_in_cal() && get_formatted_date(new Date()) == calendar_json.month.id && (new Date()).getDate() == date) {
            calendarHTML += `
            <td class="cal_cell">
              <div class="cell_row">
                <div class="cell_column">
                    <p style="text-align: center;">${date}</p>
                 </div>
                 <div class="cell_column">
                    <span class="badge badge-primary" style="color: #fff;background-color: #6c757d;">Today</span>
                </div>
              </div>
          `;
          }
          else {
            calendarHTML += `
            <td class="cal_cell">
              <div class="cell_row">
                <div class="cell_column">
                    <p style="text-align: right;">${date}</p>
                 </div>
              </div>
          `;
          }
          if (calendar_json.month[date] === undefined) {
            calendarHTML += `
              <div class="cell_row">
                <div style="text-align: center;">
                  <p>&nbsp;</p>
                </div>
              </div>
              <div class="cell_row">
                <div style="text-align: center;">
                  <p>&nbsp;</p>
                </div>
              </div>
            `;
          } else {
            const a_day = calendar_json.month[date];
            calendarHTML += `
              <div class="cell_row">
                <div>
                  <p class="event" id="${date}_hours">${convert_time_to_12_hr(a_day.start_time)} - ${convert_time_to_12_hr(a_day.end_time)}</p>
                </div>
              </div>
            `;
            if (a_day.notes === 'None') {
              calendarHTML += `
                <div class="cell_row">
                  <div style="text-align: center;">
                    <p>&nbsp;</p>
                  </div>
                </div>
              `;
            } else {
              calendarHTML += `
                <div class="cell_row">
                  <div style="text-align: center;" id="${date}_notes">
                    <a onclick="populate_cal_info(${date})">View Notes</a>
                  </div>
                </div>
              `;
            }
          }
          // Close td
          calendarHTML += '</td>';
        }
      }
      calendarHTML += '</tr>';
    }
    
    // Use calendarHTML as needed...
    
    // Close tbody and table
    calendarHTML += `</tbody></table>`;
    $("#calendar").append(calendarHTML);
}