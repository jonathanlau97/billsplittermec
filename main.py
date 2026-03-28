import streamlit as st

# ── Data ──────────────────────────────────────────────────────────────────────

BIG_LEAF = [
    {"id": "bl_01", "item": "Teh Tarik",                        "total": 4.06},
    {"id": "bl_02", "item": "Warm Water",                       "total": 0.58},
    {"id": "bl_03", "item": "Fried Chicken - Breast",           "total": 9.16},
    {"id": "bl_04", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_05", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_06", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_07", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_08", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_09", "item": "Banana Leaf Rice Meal",            "total": 14.50},
    {"id": "bl_10", "item": "Ice Water",                        "total": 0.58},
    {"id": "bl_11", "item": "Chicken 65",                       "total": 13.34},
    {"id": "bl_12", "item": "Fried Tenggiri",                   "total": 15.08},
    {"id": "bl_13", "item": "Fried Tenggiri",                   "total": 15.08},
    {"id": "bl_14", "item": "Mutton Masala",                    "total": 18.56},
    {"id": "bl_15", "item": "Chicken Varuval",                  "total": 12.64},
    {"id": "bl_16", "item": "Chicken Varuval",                  "total": 12.64},
    {"id": "bl_17", "item": "Teh Tarik",                        "total": 4.06},
    {"id": "bl_18", "item": "Tandoori Chicken Combo - Garlic Butter Naan", "total": 25.40},
    {"id": "bl_19", "item": "Coke Zero",                        "total": 4.52},
    {"id": "bl_20", "item": "Biryani Rice - Chicken Curry",     "total": 9.16},
    {"id": "bl_21", "item": "Biryani Rice - Chicken Curry",     "total": 9.16},
    {"id": "bl_22", "item": "Fried Chicken - Drumstick",        "total": 9.16},
]

ABADI = [
    {"id": "ab_01", "item": "Air Suam",          "total": 0.40},
    {"id": "ab_02", "item": "Air Suam",          "total": 0.40},
    {"id": "ab_03", "item": "Limau Ais",         "total": 3.10},
    {"id": "ab_04", "item": "Teh O Limau Ais",   "total": 3.40},
    {"id": "ab_05", "item": "Teh O Limau Ais",   "total": 3.40},
    {"id": "ab_06", "item": "Milo Ais",          "total": 4.70},
    {"id": "ab_07", "item": "Limau Panas",       "total": 2.00},
    {"id": "ab_08", "item": "Sirap Bandung Ais", "total": 3.70},
    {"id": "ab_09", "item": "Limau Ais",         "total": 3.10},
    {"id": "ab_10", "item": "Teh Tarik",         "total": 2.50},
    {"id": "ab_11", "item": "Limau Ais",         "total": 2.70},
    {"id": "ab_12", "item": "Limau Panas",       "total": 2.00},
    {"id": "ab_13", "item": "Limau Ais",         "total": 2.70},
]

# ── Session State Init ────────────────────────────────────────────────────────

if "claimed" not in st.session_state:
    st.session_state.claimed = {}   # {item_id: claimer_name}

if "pending" not in st.session_state:
    st.session_state.pending = set()  # item_ids checked but not yet submitted

# ── Helper ────────────────────────────────────────────────────────────────────

def render_receipt(title, items, grand_total):
    st.subheader(title)
    st.caption(f"Grand Total: RM {grand_total:.2f}")

    running = 0.0
    for item in items:
        iid = item["id"]
        claimed_by = st.session_state.claimed.get(iid)

        col1, col2, col3 = st.columns([0.08, 0.62, 0.30])

        if claimed_by:
            with col1:
                st.checkbox("", value=True, disabled=True, key=f"chk_{iid}")
            with col2:
                st.markdown(f"~~{item['item']}~~ — *{claimed_by}*")
            with col3:
                st.markdown(f"RM {item['total']:.2f}")
        else:
            checked = iid in st.session_state.pending
            with col1:
                ticked = st.checkbox("", value=checked, key=f"chk_{iid}")
            with col2:
                st.markdown(item["item"])
            with col3:
                st.markdown(f"RM {item['total']:.2f}")

            if ticked:
                st.session_state.pending.add(iid)
                running += item["total"]
            else:
                st.session_state.pending.discard(iid)

    return running

# ── UI ────────────────────────────────────────────────────────────────────────

st.title("🍛 Bill Splitter")
st.markdown("Select the items you ordered, enter your name, then click **Submit**.")

name = st.text_input("Your name", placeholder="e.g. Ali")

st.divider()
total_pending = 0.0
total_pending += render_receipt("🍽️ Big Leaf", BIG_LEAF, 250.20)
st.divider()
total_pending += render_receipt("☕ Abadi Cafeteria", ABADI, 34.10)
st.divider()

if total_pending > 0:
    st.success(f"**Your current selection: RM {total_pending:.2f}**")

col_submit, col_reset = st.columns([1, 1])

with col_submit:
    if st.button("✅ Submit", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Please enter your name before submitting.")
        elif not st.session_state.pending:
            st.error("Please select at least one item.")
        else:
            for iid in st.session_state.pending:
                st.session_state.claimed[iid] = name.strip()
            st.session_state.pending.clear()
            st.success(f"Items claimed by **{name.strip()}**! Total: RM {total_pending:.2f}")
            st.rerun()

with col_reset:
    if st.button("🔄 Reset All (Admin)", use_container_width=True):
        st.session_state.claimed.clear()
        st.session_state.pending.clear()
        st.rerun()

# ── Summary ───────────────────────────────────────────────────────────────────

if st.session_state.claimed:
    st.divider()
    st.subheader("📊 Summary")
    summary = {}
    all_items = BIG_LEAF + ABADI
    for item in all_items:
        claimer = st.session_state.claimed.get(item["id"])
        if claimer:
            summary[claimer] = summary.get(claimer, 0.0) + item["total"]
    for person, amt in sorted(summary.items()):
        st.markdown(f"- **{person}**: RM {amt:.2f}")
    st.markdown(f"**Total Claimed: RM {sum(summary.values()):.2f}**")
