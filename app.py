
import streamlit as st
from parser import parse_availability
import streamlit.components.v1 as components

st.set_page_config(page_title="Availability Parser + Calendar", layout="wide")
st.title("📅 NLP-Powered Teacher Availability Calendar")

st.markdown("### Step 1: Enter your availability in plain language")
text_input = st.text_area("Example: 'I'm free Monday after 2pm, weekends, and Friday mornings'",
                          "I'm free Monday after 2pm, weekends, and Friday mornings")

if st.button("Parse and Show Calendar"):
    slots = parse_availability(text_input)

    if not slots:
        st.warning("⚠️ Could not detect any time slots.")
    else:
        st.success("✅ Parsed time slots:")
        st.write(slots)

        # Convert to FullCalendar format
        day_map = {
            "Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3,
            "Thursday": 4, "Friday": 5, "Saturday": 6
        }

        fullcalendar_events = []
        for day, start, end in slots:
            fullcalendar_events.append(f"""{{
                title: 'Available',
                daysOfWeek: [{day_map[day]}],
                startTime: '{start}',
                endTime: '{end}'
            }}""")

        calendar_code = f"""
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.css' rel='stylesheet' />
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js'></script>
        <div id='calendar'></div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {{
                initialView: 'timeGridWeek',
                slotMinTime: "08:00:00",
                slotMaxTime: "20:00:00",
                allDaySlot: false,
                events: [{','.join(fullcalendar_events)}]
            }});
            calendar.render();
        }});
        </script>
        <style>
            #calendar {{ max-width: 900px; margin: 40px auto; }}
        </style>
        """
        components.html(calendar_code, height=700)
