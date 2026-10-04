import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "internalert.db")

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from database import create_database


# =========================
# GLOBAL VARIABLES
# =========================

waiting_for_search = set()
profile_setup = {}

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🔎 Find Internships",
                callback_data="find"
            )
        ],
        [
            InlineKeyboardButton(
                "🆕 Latest Internships",
                callback_data="latest"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Saved Internships",
                callback_data="saved"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 My Profile",
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                "🔔 My Alerts",
                callback_data="alerts"
            )
        ]
    ]

    await update.message.reply_text(
        "🎓 Welcome to InternAlert!\n\n"
        "Find internships and opportunities "
        "for students.\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# LATEST INTERNSHIPS
# =========================

async def show_latest_internships(query):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            stipend,
            deadline,
            apply_url
        FROM internships
        ORDER BY created_at DESC
        LIMIT 10
    """)

    internships = cursor.fetchall()
    connection.close()

    if not internships:

        await query.edit_message_text(
            "🆕 Latest Internships\n\n"
            "No internships available right now."
        )

        return

    await query.edit_message_text(
        "🆕 Latest Internships\n\n"
        "Here are the latest opportunities:"
    )

    for internship in internships:

        internship_id = internship[0]
        title = internship[1]
        company = internship[2]
        location = internship[3]
        stipend = internship[4]
        deadline = internship[5]
        apply_url = internship[6]

        text = (
            f"🆕 *{title}*\n\n"
            f"🏢 Company: {company}\n"
            f"📍 Location: {location}\n"
            f"💰 Stipend: {stipend}\n"
            f"📅 Deadline: {deadline}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Apply Now",
                    url=apply_url
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ Save",
                    callback_data=f"save_{internship_id}"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# SEARCH INTERNSHIPS
# =========================

async def search_internships(update, context):

    user_id = update.effective_user.id

    if user_id not in waiting_for_search:
        return

    waiting_for_search.remove(user_id)

    keyword = update.message.text.strip()

    if not keyword:

        await update.message.reply_text(
            "Please enter a search keyword."
        )

        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    search = f"%{keyword}%"

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            stipend,
            deadline,
            apply_url
        FROM internships
        WHERE title LIKE ?
           OR company LIKE ?
           OR location LIKE ?
           OR skills LIKE ?
           OR description LIKE ?
        ORDER BY created_at DESC
        LIMIT 10
    """, (
        search,
        search,
        search,
        search,
        search
    ))

    internships = cursor.fetchall()
    connection.close()

    if not internships:

        await update.message.reply_text(
            f"🔎 No internships found for: {keyword}"
        )

        return

    await update.message.reply_text(
        f"🔎 Found {len(internships)} "
        f"internship(s) for: {keyword}"
    )

    for internship in internships:

        internship_id = internship[0]
        title = internship[1]
        company = internship[2]
        location = internship[3]
        stipend = internship[4]
        deadline = internship[5]
        apply_url = internship[6]

        text = (
            f"🧑‍💻 *{title}*\n\n"
            f"🏢 Company: {company}\n"
            f"📍 Location: {location}\n"
            f"💰 Stipend: {stipend}\n"
            f"📅 Deadline: {deadline}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Apply Now",
                    url=apply_url
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ Save",
                    callback_data=f"save_{internship_id}"
                )
            ]
        ]

        await update.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# CATEGORY SEARCH
# =========================

async def category_search(update, context):

    query = update.callback_query
    await query.answer()

    category_map = {
        "search_python": "Python",
        "search_data_science": "Data Science",
        "search_sql": "SQL",
        "search_web": "Web Development",
        "search_remote": "Remote"
    }

    keyword = category_map.get(query.data)

    if not keyword:
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    search = f"%{keyword}%"

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            stipend,
            deadline,
            apply_url
        FROM internships
        WHERE title LIKE ?
           OR company LIKE ?
           OR location LIKE ?
           OR skills LIKE ?
           OR description LIKE ?
        ORDER BY created_at DESC
        LIMIT 10
    """, (
        search,
        search,
        search,
        search,
        search
    ))

    internships = cursor.fetchall()
    connection.close()

    if not internships:

        await query.edit_message_text(
            f"🔎 No internships found for: {keyword}"
        )

        return

    await query.edit_message_text(
        f"🔎 Found {len(internships)} "
        f"internship(s) for: {keyword}"
    )

    for internship in internships:

        internship_id = internship[0]
        title = internship[1]
        company = internship[2]
        location = internship[3]
        stipend = internship[4]
        deadline = internship[5]
        apply_url = internship[6]

        text = (
            f"🧑‍💻 *{title}*\n\n"
            f"🏢 Company: {company}\n"
            f"📍 Location: {location}\n"
            f"💰 Stipend: {stipend}\n"
            f"📅 Deadline: {deadline}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Apply Now",
                    url=apply_url
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ Save",
                    callback_data=f"save_{internship_id}"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# SAVED INTERNSHIPS
# =========================

async def show_saved_internships(query):

    user_id = query.from_user.id

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            internships.id,
            internships.title,
            internships.company,
            internships.location,
            internships.stipend,
            internships.deadline,
            internships.apply_url
        FROM saved_internships
        JOIN internships
            ON saved_internships.internship_id = internships.id
        WHERE saved_internships.user_id = ?
        ORDER BY saved_internships.saved_at DESC
    """, (user_id,))

    internships = cursor.fetchall()
    connection.close()

    if not internships:

        await query.edit_message_text(
            "⭐ Saved Internships\n\n"
            "You haven't saved any internships yet.\n\n"
            "Go to 🆕 Latest Internships and "
            "tap ⭐ Save on an internship."
        )

        return

    await query.edit_message_text(
        f"⭐ You have saved {len(internships)} "
        f"internship(s):"
    )

    for internship in internships:

        internship_id = internship[0]
        title = internship[1]
        company = internship[2]
        location = internship[3]
        stipend = internship[4]
        deadline = internship[5]
        apply_url = internship[6]

        text = (
            f"⭐ *{title}*\n\n"
            f"🏢 Company: {company}\n"
            f"📍 Location: {location}\n"
            f"💰 Stipend: {stipend}\n"
            f"📅 Deadline: {deadline}"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Apply Now",
                    url=apply_url
                )
            ],
            [
                InlineKeyboardButton(
                    "🗑 Remove",
                    callback_data=f"remove_{internship_id}"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


# =========================
# SAVE INTERNSHIP
# =========================

async def save_internship(update, context):

    query = update.callback_query

    user_id = query.from_user.id

    internship_id = int(
        query.data.split("_")[1]
    )

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO saved_internships
        (user_id, internship_id)
        VALUES (?, ?)
    """, (
        user_id,
        internship_id
    ))

    connection.commit()
    connection.close()

    await query.answer(
        "⭐ Internship saved!",
        show_alert=True
    )


# =========================
# REMOVE SAVED INTERNSHIP
# =========================

async def remove_saved_internship(update, context):

    query = update.callback_query

    user_id = query.from_user.id

    internship_id = int(
        query.data.split("_")[1]
    )

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM saved_internships
        WHERE user_id = ?
          AND internship_id = ?
    """, (
        user_id,
        internship_id
    ))

    connection.commit()
    connection.close()

    await query.answer(
        "🗑 Internship removed from saved!",
        show_alert=True
    )

    await show_saved_internships(query)


# =========================
# PROFILE SETUP
# =========================

async def profile_setup_handler(update, context):

    user_id = update.effective_user.id

    if user_id not in profile_setup:
        return False

    text = update.message.text.strip()

    step = profile_setup[user_id]["step"]

    # NAME
    if step == "name":

        profile_setup[user_id]["name"] = text
        profile_setup[user_id]["step"] = "degree"

        await update.message.reply_text(
            "🎓 Step 2 of 5\n\n"
            "What is your degree?\n\n"
            "Example: B.Tech CSE - Data Science"
        )

    # DEGREE
    elif step == "degree":

        profile_setup[user_id]["degree"] = text
        profile_setup[user_id]["step"] = "skills"

        await update.message.reply_text(
            "💻 Step 3 of 5\n\n"
            "What are your skills?\n\n"
            "Example: Python, SQL, Excel, Power BI"
        )

    # SKILLS
    elif step == "skills":

        profile_setup[user_id]["skills"] = text
        profile_setup[user_id]["step"] = "location"

        await update.message.reply_text(
            "📍 Step 4 of 5\n\n"
            "What is your preferred internship location?\n\n"
            "Example: Hyderabad, Bangalore, Remote"
        )

    # LOCATION
    elif step == "location":

        profile_setup[user_id]["location"] = text
        profile_setup[user_id]["step"] = "remote"

        await update.message.reply_text(
            "🏠 Step 5 of 5\n\n"
            "Do you prefer remote internships?\n\n"
            "Reply with:\n"
            "Yes or No"
        )

    # REMOTE
    elif step == "remote":

        profile_setup[user_id]["remote_preference"] = text

        profile = profile_setup[user_id]

        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO users
            (
                user_id,
                name,
                degree,
                skills,
                location,
                remote_preference
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            profile["name"],
            profile["degree"],
            profile["skills"],
            profile["location"],
            profile["remote_preference"]
        ))

        connection.commit()
        connection.close()

        del profile_setup[user_id]

        await update.message.reply_text(
            "✅ Profile Created Successfully!\n\n"
            f"👤 Name: {profile['name']}\n"
            f"🎓 Degree: {profile['degree']}\n"
            f"💻 Skills: {profile['skills']}\n"
            f"📍 Location: {profile['location']}\n"
            f"🏠 Remote: {profile['remote_preference']}"
        )

    return True


# =========================
# TEXT MESSAGE ROUTER
# =========================

async def text_message_handler(update, context):

    user_id = update.effective_user.id

    # Profile setup gets priority
    if user_id in profile_setup:

        await profile_setup_handler(update, context)
        return

    # Manual internship search
    if user_id in waiting_for_search:

        await search_internships(update, context)
        return


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update, context):

    query = update.callback_query

    await query.answer()

    # FIND
    if query.data == "find":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🐍 Python",
                    callback_data="search_python"
                )
            ],
            [
                InlineKeyboardButton(
                    "📊 Data Science",
                    callback_data="search_data_science"
                )
            ],
            [
                InlineKeyboardButton(
                    "🗄 SQL",
                    callback_data="search_sql"
                )
            ],
            [
                InlineKeyboardButton(
                    "🌐 Web Development",
                    callback_data="search_web"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Remote",
                    callback_data="search_remote"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔍 Other / Type Manually",
                    callback_data="search_other"
                )
            ]
        ]

        await query.edit_message_text(
            "🔎 *Find Internships*\n\n"
            "What are you looking for?\n\n"
            "Choose an option:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # LATEST
    elif query.data == "latest":

        await show_latest_internships(query)

    # SAVED
    elif query.data == "saved":

        await show_saved_internships(query)

    # PROFILE
    elif query.data == "profile":

        user_id = query.from_user.id

        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                name,
                degree,
                skills,
                location,
                remote_preference
            FROM users
            WHERE user_id = ?
        """, (user_id,))

        user = cursor.fetchone()

        connection.close()

        if not user:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "📝 Create Profile",
                        callback_data="create_profile"
                    )
                ]
            ]

            await query.edit_message_text(
                "👤 My Profile\n\n"
                "Your profile is not created yet.\n\n"
                "Create your profile to get personalized "
                "internship recommendations.",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            return

        name = user[0] or "Not set"
        degree = user[1] or "Not set"
        skills = user[2] or "Not set"
        location = user[3] or "Not set"
        remote = user[4] or "Not set"

        await query.edit_message_text(
            f"👤 *My Profile*\n\n"
            f"👤 Name: {name}\n"
            f"🎓 Degree: {degree}\n"
            f"💻 Skills: {skills}\n"
            f"📍 Location: {location}\n"
            f"🏠 Remote: {remote}",
            parse_mode="Markdown"
        )

    # CREATE PROFILE
    elif query.data == "create_profile":

        user_id = query.from_user.id

        profile_setup[user_id] = {
            "step": "name"
        }

        await query.edit_message_text(
            "📝 *Create Your Profile*\n\n"
            "Step 1 of 5\n\n"
            "👤 What is your name?",
            parse_mode="Markdown"
        )

    # MANUAL SEARCH
    elif query.data == "search_other":

        user_id = query.from_user.id

        waiting_for_search.add(user_id)

        await query.edit_message_text(
            "🔍 *Manual Search*\n\n"
            "Type the internship role, skill, "
            "company, or location you are looking for.\n\n"
            "Examples:\n"
            "• Machine Learning\n"
            "• Java\n"
            "• Hyderabad\n"
            "• Data Analyst\n"
            "• Microsoft",
            parse_mode="Markdown"
        )

    # ALERTS
    elif query.data == "alerts":

        await query.edit_message_text(
            "🔔 My Alerts\n\n"
            "Your internship alerts will appear here."
        )


# =========================
# MAIN
# =========================

def main():

    create_database()

    if not TOKEN:

        raise ValueError(
            "Please set TELEGRAM_BOT_TOKEN first."
        )

    app = Application.builder().token(TOKEN).build()

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # Main buttons
    app.add_handler(
        CallbackQueryHandler(
            button_handler,
            pattern="^(find|latest|saved|profile|alerts|create_profile|search_other)$"
        )
    )

    # Category search
    app.add_handler(
        CallbackQueryHandler(
            category_search,
            pattern="^search_(python|data_science|sql|web|remote)$"
        )
    )

    # Save
    app.add_handler(
        CallbackQueryHandler(
            save_internship,
            pattern="^save_[0-9]+$"
        )
    )

    # Remove
    app.add_handler(
        CallbackQueryHandler(
            remove_saved_internship,
            pattern="^remove_[0-9]+$"
        )
    )

    # Normal text
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_message_handler
        )
    )

    print("InternAlert is running...")

    app.run_polling()


# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
    main()