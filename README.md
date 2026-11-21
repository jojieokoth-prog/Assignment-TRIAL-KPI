# Mini KPI dashboard: share your pandas work as a private web app

In this add-on you turn a cleaned CSV into a one-page dashboard: **3 KPI tiles, 1 chart and a dropdown filter**. You publish it free on Streamlit Community Cloud as a **private app** that only the classmates you invite can open.

Time needed: about 30 minutes. You need a GitHub account (free) and the three files below.

![The finished dashboard](screenshot.png)

---

## 1. The three files

Put these three files together in one folder:

| File | What it is |
|---|---|
| `app.py` | The dashboard (29 lines of Python) |
| `requirements.txt` | The packages the server must install: `streamlit` and `pandas` |
| `daily_operations.csv` | The data (fictional daily operations at 6 stations in 2025) |

### The full code of `app.py`

```python
import streamlit as st
import pandas as pd

# 1. Page setup
st.set_page_config(page_title="Rail KPI Dashboard", layout="wide")
st.title("Rail KPI Dashboard 2025")  # <- your title
st.caption("Fictional data: daily operations at 6 stations in 2025")  # <- your subtitle

# 2. Load the data (the CSV sits in the same folder as app.py)
df = pd.read_csv("daily_operations.csv")  # <- your CSV file name
df["date"] = pd.to_datetime(df["date"])

# 3. Station dropdown
stations = ["All stations"] + sorted(df["station"].unique())
choice = st.selectbox("Station", stations)
if choice != "All stations":
    df = df[df["station"] == choice]

# 4. Three KPI tiles
col1, col2, col3 = st.columns(3)
col1.metric("Total passengers", f"{df['passengers'].sum():,}", border=True)
col2.metric("Punctuality rate", f"{df['punctuality_rate'].mean():.1f} %", border=True)
col3.metric("Average delay", f"{df['avg_delay_minutes'].mean():.1f} min", border=True)

# 5. One chart: average punctuality rate per month
df["month"] = df["date"].dt.month
monthly = df.groupby("month")["punctuality_rate"].mean()
st.subheader("Punctuality rate by month (%)")
st.bar_chart(monthly, x_label="Month (1 = January)", y_label="Punctuality rate (%)", height=450)
```

### What `app.py` does, block by block

1. **Page setup**: wide layout, a title and a subtitle.
2. **Load the data**: `pd.read_csv()` reads the CSV, `pd.to_datetime()` turns the date column into real dates.
3. **Station dropdown**: `st.selectbox()` shows "All stations" plus every station. If one station is chosen, the table is filtered with `df[df["station"] == choice]`.
4. **Three KPI tiles**: `st.columns(3)` makes three columns, and `st.metric()` shows one number in each: total passengers (`sum`), punctuality rate (`mean`) and average delay (`mean`).
5. **One chart**: `.dt.month` takes the month from each date, `groupby("month")` with `mean()` gives one value per month, and `st.bar_chart()` draws it.

Everything that changes the numbers is pandas you already know. Streamlit only displays the results.

### Using your own CSV

1. Change the three lines marked `# <-` (title, subtitle, CSV file name).
2. Change the column names in blocks 3, 4 and 5 to the columns in your data.
3. Check your column names first with `print(df.columns)` in your notebook. Names must match exactly, including capital letters.

---

## 2. Step A: put the files on GitHub (private repository)

1. Sign in at github.com and click **New** (or the **+** at the top right, then **New repository**).
2. Give it a name, for example `minikpi`.
3. Choose **Private**. Leave everything else as it is and click **Create repository**.
4. On the new page, click **uploading an existing file**.
5. Drag in `app.py`, `requirements.txt` and your CSV, then click **Commit changes**.

All three files must sit at the top level of the repository, not inside a subfolder.

---

## 3. Step B: deploy on Streamlit Community Cloud

### B1. Sign in and allow access to private repositories

1. Go to **share.streamlit.io** and sign in with your GitHub account. Follow the prompts and click **Authorize streamlit**.
2. Allow Streamlit to read your **private** repositories. Do this even if you have used Streamlit before: signing in only gives access to public repositories, so without this step your private repository is invisible to Streamlit.
   - Click your username at the top left, then **Settings**.
   - Choose **Linked accounts** on the left.
   - Under **Source control**, click **Connect here** (or the link to update your GitHub permissions).
   - GitHub asks for access to your private repositories. Click **Authorize streamlit**.

### B2. Create the app

1. Click **Create app** at the top right.
2. On the page "What would you like to do?", choose **Deploy a public app from GitHub** and click **Deploy now**. Do not worry about the word "public": an app made from a private repository is private (you check this in B3). The Snowflake option is a paid trial and the template option starts from a sample app, so skip both.
3. On the page "Deploy an app", fill in:
   - **Repository**: `yourname/minikpi`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): a short name, for example `yourname-minikpi`
4. When all fields are accepted (no red messages), click **Deploy**. The first start takes a few minutes while the packages are installed.

If the page says **"This repository does not exist"**, **"This branch does not exist"** and **"This file does not exist"** all at once, your repository is fine: Streamlit simply cannot see private repositories yet. Go back to step B1.2, then reload the "Deploy an app" page and fill it in again. If the messages stay, see the troubleshooting table in section 7.

### B3. Check that the app is private

Open your app, click **Share** (or **App settings**, then **Sharing**). It should say **Only specific people can view this app**. If it says the app is public, choose **Only specific people can view this app** there.

---

## 4. Step C: share the app with classmates

1. Open your app and click **Share** at the top right.
2. Type a classmate's email address and click **Invite**. Repeat for each classmate.
3. Each classmate gets an email with a link. They sign in with Google if their email is a Google account, or with a one-time link sent by email. They do not need a GitHub or Streamlit account.

To remove someone, open **Share** again and click the cross next to their name.

---

## 5. Updating the app

Upload the changed file to the same GitHub repository (**Add file**, then **Upload files**, then **Commit changes**). The app picks up the change by itself within a minute or two.

---

## 6. Good to know

- **One private app per account.** Each Community Cloud account can have only one private app at a time. To make a second private app, first delete the old one or make it public.
- **Viewers can invite others.** Anyone you invite can also invite more people, and they can see the email addresses of the other viewers in the app's analytics. Invite only people who are happy to share their email with the group.
- **Sleeping apps.** An app that nobody visits for 12 hours goes to sleep. The next visitor clicks **Yes, get this app back up!** and it is back after a short wait. Any invited viewer can do this.
- **Fictional data.** Never put real personal or confidential data in a class project, even in a private app.

---

## 7. Troubleshooting

| What you see | Usual cause | Fix |
|---|---|---|
| "This repository does not exist" (plus branch and file) when deploying | Streamlit has no access to your private repositories | Do step B1.2 and reload the page. Still failing: on GitHub open your picture, **Settings**, **Applications**, **Authorized OAuth Apps**, **Streamlit**, click **Revoke**, then sign in to share.streamlit.io again and accept the request for private repositories |
| Red messages on the deploy page and you are not sure the names are right | A typing mistake (the repository must be exactly `username/repository`) | Use **Paste GitHub URL** on the deploy page and paste the address of your `app.py` on GitHub |
| `ModuleNotFoundError` | A package is missing from `requirements.txt` | Add its name on a new line and upload the file again |
| `FileNotFoundError` | The CSV name in `app.py` does not match the file on GitHub | Check spelling and capital letters, and that the CSV is at the top level |
| `KeyError: 'passengers'` | A column name does not exist in your CSV | Use the exact names from `print(df.columns)` |
| The app is stuck on "Your app is in the oven" | The first install is still running | Wait a few minutes, then refresh |

To see the full error, open **Manage app** at the bottom right of your app.

---

## 8. Other ways to publish (for reference)

| Option | Private? | Cost | Code? | Notes |
|---|---|---|---|---|
| **A. Streamlit private app** (this guide) | Yes, by email invite | Free | Yes | One private app per account |
| **B. Streamlit public app with a password** | Only by shared password | Free | Yes | Use when your private slot is taken |
| **C. Run on your own laptop** | Only people on the same Wi-Fi | Free | Yes | Works only while your laptop is on |
| **D. Google Looker Studio** | Yes, by email | Free | No | Drag-and-drop dashboard, no pandas |
| **E. Google Colab notebook** | Yes, by email | Free | Yes | Shares the notebook, not a dashboard |
| **F. Hugging Face Spaces** | Owner or organisation only | Free | Yes | Streamlit template, harder to share privately |
| **G. Google Cloud Run** | Yes, with login control | Free tier, needs a credit card | Yes | Professional hosting, too complex for this task |

### B. Public app with a password

Add these three lines to `app.py`, right after `st.set_page_config(...)`:

```python
password = st.text_input("Password", type="password")
if password != st.secrets["password"]:
    st.stop()
```

When you deploy, open **Advanced settings** and type this into the **Secrets** box (with your own password):

```toml
password = "choose_a_password"
```

The password stays out of your code. Use a **public** repository for this option, or your private slot is used up. Anyone with the link and the password can open the app.

### C. Run on your own laptop (same Wi-Fi)

In a terminal, inside the folder with `app.py`:

```
pip install streamlit pandas
streamlit run app.py
```

Streamlit prints two addresses. **Local URL** opens the app on your own computer. **Network URL** (for example `http://192.168.0.12:8501`) can be opened by classmates on the same Wi-Fi network. It stops working when you close the terminal or the laptop. On university or public Wi-Fi, the network or your firewall may block it.

### D. Google Looker Studio

Go to lookerstudio.google.com, create a report and add your CSV with the **File Upload** connector (or put it in Google Sheets first). Add three **Scorecard** charts, one **Bar chart** and a **Drop-down list** control. Share it like a Google Doc. It is the easiest private sharing of all, but there is no Python in it.

### E. Google Colab

Put your pandas code and a plot in a Colab notebook and use **Share** to invite classmates by email. Good for showing your code, but readers see a notebook, not a dashboard.

### F. Hugging Face Spaces

Create a Space with the Streamlit template and upload the same three files. A private Space can only be opened by you or members of your Hugging Face organisation, so sharing with classmates means everyone needs an account and joins an organisation.

### G. Google Cloud Run

Runs your app as a container on Google Cloud, with Google sign-in control. It needs a billing account and command-line setup, so it is mentioned here only for completeness.

---

## 9. Sources

Checked on 24 October 2026. Button names and limits can change, so check the official pages if something looks different.

**Streamlit Community Cloud**

- [Deploy your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Connect your GitHub account](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account)
- [Share your app](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)
- [Manage your app (app hibernation)](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)
- [Secrets management for your Community Cloud app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Status and limitations of Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/status)

**Streamlit and pandas functions used in app.py**

- [st.metric](https://docs.streamlit.io/develop/api-reference/data/st.metric)
- [st.selectbox](https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox)
- [st.bar_chart](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart)
- [pandas documentation](https://pandas.pydata.org/docs/)

**GitHub**

- [Adding a file to a repository](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

**Other options**

- [Hugging Face: Streamlit Spaces](https://huggingface.co/docs/hub/spaces-sdks-streamlit)
- [Looker Studio Help](https://support.google.com/looker-studio)
- [Google Colab](https://colab.research.google.com)
- [Google Cloud Run documentation](https://cloud.google.com/run/docs)

---

___
**END**
