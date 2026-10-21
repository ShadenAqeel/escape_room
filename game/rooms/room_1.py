import streamlit as st
import navigations 

from pathlib import Path
import time
import base64

# Python script for the basement room: all related functions (puzzles) and the page interface 

@st.cache_data(show_spinner=False)
def cached_picture(image_path, modified_time):
    # Convert once, then reuse until the image changes.
    return base64.b64encode(
        Path(image_path).read_bytes()
    ).decode("utf-8")


def show_picture(file_name, max_width=360):
    root = Path(__file__).resolve().parents[2]
    image_path = root / "assets" / "images" / "room_1" / file_name

    picture = cached_picture(
        str(image_path),
        image_path.stat().st_mtime_ns
    )

    # Room 1 already has separate puzzle pictures, so no cropping is needed.
    st.markdown(
        f"""
        <div style="
            width: min(100%, {max_width}px);
            margin: .4rem auto 1rem;
            overflow: hidden;
            border-radius: 9px;
            border: 1px solid #68665f;
        ">
            <img
                src="data:image/webp;base64,{picture}"
                alt="Puzzle close-up"
                style="width:100%; height:auto; display:block;"
            >
        </div>
        """,
        unsafe_allow_html=True
    )




# ------------------------------------ Puzzle Functions (Logic part) ------------------------------------

# 1. First puzzle 
# Power generator puzzle function 
# The user needs to activate all five switches to turn on the power.

# List to store the correct sequence of turning the switches on (correct is: switch 3, 1, 4, 2, then 5)
correct_switches_order = [3, 1, 4, 2, 5]

# A list to save the player's order for turning the Switch on.
current_switches_order = []

# Turn on the switch if it is the correct next switch 
def turn_switch(switches, correct_switches_order, current_switches_order, switch_number):

    # If the switch chosed by player is the correct one add it to the current_order list 
    if switch_number == correct_switches_order[len(current_switches_order)] : 
        switches[switch_number - 1] = True # Turn the switch to True 
        current_switches_order.append(switch_number) # Append to the current switches order list
        return True
    # Return False 
    return False


# Reset function that reset all generator's switches to off (False)
def reset_generator():
    return [False for x in range(5)]

# 2. Second puzzle 
# The other puzzle is finding the correct answer to the equations (the player should enter three correct numbers)

# Tuple to store the counts of the shapes in the puzzle tha player should counts 
shapes_counts = (3, 3, 3, 2)


shape1_count =  shapes_counts[0] # Hilal icon (outlined)
shape2_count =  shapes_counts[1] # Hilal icon (filled)
shape3_count = shapes_counts[2] # star icon (filled)
shape4_count = shapes_counts[3] # Sun icon (outlined)

answers = []

# Here adding the answer of the calculations to the answer list (these calculations from the note)
answers.append(shape1_count * shape3_count)
answers.append(shape4_count + shape2_count)
answers.append(shape3_count - shape4_count)

# Reconvert to tuple 
answers = tuple(answers)

# Check player answer
def check_answer(player_answer):

    for i in range(3):
        # IF one of the answer is False return False (not solved)
        if player_answer[i] != answers[i]:
            return False
    return True


# 3. Third puzzle 
# Mirror puzzle function 

# The puzzle here is that the mirrors consist of three vertical segments; 
# the player must adjust them so they all face the right direction, 
# revealing a phrase that helps with the final solution.


# This is the current status of the mirror parts that will apears to the player 
mirror_parts_status = [False, True, False]

def rotate_mirror(mirror_parts_status, mirror_number):
    if mirror_parts_status[mirror_number - 1] == True:
        mirror_parts_status[mirror_number - 1] = not True 
    else : 
        mirror_parts_status[mirror_number - 1] = True   

def check_mirror(mirror_parts_status): 
    for i in mirror_parts_status:
        if i == False :
            return False 
    return True

def return_rotation_angle(mirror_parts_status, mirror_number): 
    if mirror_parts_status[mirror_number - 1] == True:
        return 0
    else : 
        return 180 

# 4. Final Puzzle (KEY CABINET)
# Function to check if player get the correct code to open the KEY CABINET to get the key
def check_code(player_code):
    if player_code == "159":
        return True 
    else: 
        return False 

# ------------------------------------ Interface Part (Streamlit) ------------------------------------

# Streamlit session stat for retaining values between reruns for the same user
def setup():

    # Store the switches state
    if "switches" not in st.session_state:
        st.session_state.switches = reset_generator()

    # Store the player's current order
    if "current_order" not in st.session_state:
        st.session_state.current_order = []

    # Store whether the player selected a wrong switch
    if "wrong_switch" not in st.session_state:
        st.session_state.wrong_switch = False

    # Store the status of the mirrors
    if "mirror_parts_status" not in st.session_state:
        if navigations.is_solved("mirror"):
            st.session_state.mirror_parts_status = [True, True, True]
        else:
            st.session_state.mirror_parts_status = [False, True, False]

    # Store whether the generator popup is open
    if "generator_open" not in st.session_state:
        st.session_state.generator_open = False

    # Store whether the boxes popup is open
    if "boxes_open" not in st.session_state:
        st.session_state.boxes_open = False

    # Store whether the mirror popup is open
    if "mirror_open" not in st.session_state:
        st.session_state.mirror_open = False

    # Store whether the key popup is open
    if "key_open" not in st.session_state:
        st.session_state.key_open = False

    if "key_cabinet_opened" not in st.session_state:
        st.session_state.key_cabinet_opened = navigations.is_solved("key")

# Styling the popup 
def apply_style():
    st.markdown(
        """
        <style>
        div[data-testid="stDialog"] div[role="dialog"] {
            background-color: #252826;
            border: 1px solid rgba(255, 255, 255, .15);
            border-radius: 12px;
        }

        div[data-testid="stDialog"] button[kind="primary"] {
            background-color: #5f6959;
            color: #f1eee6;
            border: 1px solid #747f6d;
            border-radius: 8px;
        }

        div[data-testid="stDialog"] button[kind="primary"]:hover {
            background-color: #6c7765;
            color: #ffffff;
            border-color: #899482;
        }

        div[data-testid="stDialog"] .stButton > button,
        div[data-testid="stDialog"] .stFormSubmitButton > button {
            min-height: 44px;
            border-radius: 8px;
        }

        .st-key-generator_switch_controls button {
            width: 100% !important;
            height: 44px !important;
            min-height: 44px !important;
            padding: 0 4px !important;
        }

        .st-key-generator_switch_controls button p {
            font-size: 14px !important;
            white-space: nowrap !important;
        }

        /* Keep popup input fields visible before clicking. */
        div[data-testid="stDialog"] [data-testid="stTextInput"] {
            opacity: 1 !important;
        }

        div[data-testid="stDialog"]
        [data-testid="stTextInput"] [data-baseweb="input"] {
            background-color: #353a35 !important;
            border: 1px solid #9aa58f !important;
            border-radius: 8px !important;
        }

        div[data-testid="stDialog"]
        [data-testid="stTextInput"] input {
            background-color: #353a35 !important;
            color: #f1eee6 !important;
            -webkit-text-fill-color: #f1eee6 !important;
            caret-color: #f1eee6 !important;
            opacity: 1 !important;
        }

        div[data-testid="stDialog"]
        [data-testid="stTextInput"] input::placeholder {
            color: #bfc5b8 !important;
            -webkit-text-fill-color: #bfc5b8 !important;
            opacity: 1 !important;
        }

        div[data-testid="stDialog"]
        [data-testid="stTextInput"] label,
        div[data-testid="stDialog"]
        [data-testid="stTextInput"] label p {
            color: #f1eee6 !important;
        }

        div[data-testid="stDialog"]
        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
            border-color: #c4d3b4 !important;
            box-shadow: 0 0 0 2px #c4d3b433 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def close_generator_popup():
    st.session_state.generator_open = False

def close_boxes_popup():
    st.session_state.boxes_open = False

def close_mirror_popup():
    st.session_state.mirror_open = False

def close_key_popup():
    st.session_state.key_open = False

# Generator Popup Interface  
# Update the switches before the controls redraw.
def press_generator_switch(switch_number):
    st.session_state.wrong_switch = False

    # Ignore switches that are already on.
    if st.session_state.switches[switch_number - 1]:
        return

    correct = turn_switch(
        st.session_state.switches,
        correct_switches_order,
        st.session_state.current_order,
        switch_number
    )

    if not correct:
        st.session_state.switches = reset_generator()
        st.session_state.current_order = []
        st.session_state.wrong_switch = True


def reset_generator_controls():
    st.session_state.switches = reset_generator()
    st.session_state.current_order = []
    st.session_state.wrong_switch = False


# Only these controls redraw when a switch is pressed.
@st.fragment
def generator_controls():
    with st.container(key="generator_switch_controls"):
        columns = st.columns(5, gap="small")

        for i, column in enumerate(columns):
            with column:
                is_on = st.session_state.switches[i]

    

                st.button(
                    "ON" if is_on else "OFF",
                    key=f"switch_{i + 1}",
                    use_container_width=True,
                    disabled=is_on,
                    on_click=press_generator_switch,
                    args=(i + 1,)
                )

    # Keep this space reserved so messages don't move the buttons.
    message = st.empty()

    if st.session_state.wrong_switch:
        message.error("Wrong sequence. The switches have reset.")
    else:
        message.caption(
            "Follow the note and activate the switches in order."
        )

    if st.button(
        "Start generator",
        type="primary",
        icon=":material/power_settings_new:",
        use_container_width=True,
        key="generator_start"
    ):
        if all(st.session_state.switches):
            navigations.mark_solved("generator")
            st.success("Correct sequence! The generator is running.")

            time.sleep(2.5)

            close_generator_popup()
            st.session_state.page = "basement2"
            st.rerun()
        else:
            message.error("Complete the startup sequence first.")

    st.button(
        "Reset switches",
        icon=":material/restart_alt:",
        use_container_width=True,
        key="generator_reset",
        on_click=reset_generator_controls
    )


# Generator Popup Interface
@st.dialog(
    "Emergency Generator",
    width="small",
    on_dismiss=close_generator_popup
)
def generator_popup():
    apply_style()

    st.caption("Find the correct startup sequence.")

    show_picture("generator_note_puzzle.webp")

    generator_controls()



# Boxes Popup Interface 
# Update only the answer controls when submitted.
@st.fragment
def boxes_controls():
    with st.form("storage_boxes_form"):
        columns = st.columns(3)

        with columns[0]:
            answer_1 = st.text_input("Number 1")

        with columns[1]:
            answer_2 = st.text_input("Number 2")

        with columns[2]:
            answer_3 = st.text_input("Number 3")

        submitted = st.form_submit_button(
            "Submit",
            type="primary",
            use_container_width=True
        )

    if submitted:
        if not (
            answer_1.isdigit()
            and answer_2.isdigit()
            and answer_3.isdigit()
        ):
            st.error("Enter all three answers.")
        else:
            player_answer = (
                int(answer_1),
                int(answer_2),
                int(answer_3)
            )

            if check_answer(player_answer):
                navigations.mark_solved("boxes")
                st.success("Correct! You solved the storage boxes puzzle.")

                time.sleep(2.5)

                close_boxes_popup()
                st.rerun()

@st.dialog(
    "Storage Boxes",
    width="small",
    on_dismiss=close_boxes_popup
)
def boxes_popup():
    apply_style()
    st.caption("Check the inspection labels and solve the equations.")
    show_picture("boxes_note_puzzle.webp")
    boxes_controls()

# Mirror Popup Interface  
@st.dialog("Mirror", width="small", on_dismiss=close_mirror_popup)
def mirror_popup(): 
    apply_style()
    st.caption("The reflection doesn't look right.")

    # Root path 
    ROOT = Path(__file__).resolve().parents[2]

    # Display the solved mirror
    if check_mirror(st.session_state.mirror_parts_status):

        # Connect the solved puzzle to the game navigation
        navigations.mark_solved("mirror")

        show_picture("mirror_wholePart.webp")

        st.html(
            """
            <div style="
                width: 100%;
                box-sizing: border-box;
                margin-top: 16px;
                padding: 14px 18px;
                text-align: center;
                background: #5f6959;
                color: #f1eee6;
                border: 1px solid #747f6d;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.08em;
            ">
                REVERSE WHAT YOU FOUND TO OPEN THE KEY CABINET
            </div>
            """
        )

        return

    # Set three columns for each part of the mirror 
    col1, col2, col3 = st.columns(3, gap="small")

    with col1: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_1.webp",1)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_1", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 1)
            st.rerun(scope="fragment")

    with col2: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_2.webp",2)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_2", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 2)
            st.rerun(scope="fragment")

    
    with col3: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_3.webp",3)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_3", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 3)
            st.rerun(scope="fragment")


# Key Cabinet Popup Interface  
# Key Cabinet Popup Interface
@st.dialog("Key Cabinet", width="small", on_dismiss=close_key_popup)
def key_popup():
    apply_style()

    st.caption("A three-digit lock secures the cabinet.")

    if st.session_state.key_cabinet_opened:
        show_picture("key.webp", max_width=250)
    else:
        show_picture("key_cabinet.webp", max_width=250)

    # Set three columns for each input code from the player
    col1, col2, col3 = st.columns(3, gap="small")

    with col1: 
        digit_1 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_1",
                                label_visibility="collapsed")

    with col2: 
        digit_2 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_2",
                                label_visibility="collapsed")

    with col3: 
        digit_3 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_3",
                                label_visibility="collapsed")

    st.markdown(":material/lightbulb: Use what you discovered in the basement.",text_alignment="center")

    # Concatenate the digits entered by player 
    str_code = digit_1 + digit_2 + digit_3

    # Store True or False 
    code_correct = check_code(str_code)

    open_cabinet_button, back_button = st.columns([1.35, 1],gap="small")

    with open_cabinet_button:
        open_cabinet_button = st.button("Open cabinet", type="primary", use_container_width=True)
    
    with back_button:
        back_button = st.button("Back",use_container_width=True)
    
    if open_cabinet_button:
        if not (digit_1.isdigit() and digit_2.isdigit() and digit_3.isdigit()):
            st.error("Enter the full three-digit code.")
        elif code_correct:
            #st.success("The cabinet unlocks.")
            st.session_state.key_cabinet_opened = True

            # Connect the key to app.py so the basement door can open
            navigations.mark_solved("key")

            st.rerun(scope="fragment")
        else:
            st.error("Incorrect code. Try again.")
    
    if back_button:
        st.session_state.key_open = False
        st.rerun()

    if st.session_state.key_cabinet_opened:
        st.success("The cabinet unlocks. You found the basement key.")
        
        if st.button("Continue to the living room",
                     type="primary",
                     key="basement_reward_continue",
                     width="stretch"
                     
        ):
            # Close the Basement popup
            st.session_state.key_open = False

            # Show the Living Room story message first
            st.session_state.room = "majlis"
            st.session_state.page = "message"

            st.rerun()

    


# Helper function (to display the mirror parts)
def display_mirror_image(image_path, mirror_number):
    import base64
    rotation_angle = return_rotation_angle(
        st.session_state.mirror_parts_status, mirror_number
    )

    # Convert the image to Base64 to use in HTML 
    with open(image_path, "rb") as image_file:
        image_html = base64.b64encode(image_file.read()).decode("utf-8")

    # Display the image with the correct rotation 
    st.html(
        f"""
        <img
            src="data:image/webp;base64,{image_html}"
            style="
                width: 100%;
                height: auto;
                display: block;
                transform: rotate({rotation_angle}deg);
            "
        >
        """
    )
        