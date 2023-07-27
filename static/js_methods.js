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