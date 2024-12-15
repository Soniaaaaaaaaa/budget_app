import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime
from src.budget_management import get_all_budgets, get_expenses, add_budget, delete_budget, edit_budget, add_expense, delete_expense, edit_expense
from src.users import get_user_info, edit_user, user_login, user_register, validate_token
from src.groups import get_group_info, edit_group, create_group, add_member, delete_member, view_members
from src.analytics import get_expenses_by_group, create_report, get_reports_by_group, get_report_by_id
from src.purchase_planning import view_shopping_lists, view_items, add_item, add_list, delete_item, delete_list, get_propositions


def login():
    if 'group_id' in st.session_state:
        del st.session_state.group_id
    if 'edit_group' in st.session_state:
        del st.session_state.edit_group
    if 'edit_profile' in st.session_state:
        del st.session_state.edit_profile
    if 'create_group' in st.session_state:
        del st.session_state.create_group
    if 'create_report' in st.session_state:
        del st.session_state.create_report
    if 'edit_budget_id' in st.session_state:
        del st.session_state.edit_budget_id
        del st.session_state.edit_budget_name
        del st.session_state.edit_total_budget
    if 'current_budget' in st.session_state:
        del st.session_state.current_budget
    if 'edit_expense_id' in st.session_state:
        del st.session_state.edit_expense_id
        del st.session_state.edit_expense_description
        del st.session_state.edit_expense_price
        del st.session_state.edit_expense_expense_type
        del st.session_state.edit_expense_category_id
    if 'current_list' in st.session_state:
        del st.session_state.current_list
        del st.session_state.current_list_name
        del st.session_state.current_list_balance
    if 'report_id' in st.session_state:
        del st.session_state.report_id
    if 'add_item' in st.session_state:
        del st.session_state.add_item

    if 'register_flg' not in st.session_state:
        st.title('Welcome back!')
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')

            if st.form_submit_button("Log in"):
                result = user_login(email, password)
                if result:
                    st.session_state.user_id = result['id']
                    st.session_state.jwt_token = result['token']
                    st.rerun()
                else:
                    st.error('Invalid credentials')

        col1, col2, _, _ = st.columns(4, vertical_alignment='center')

        with col1:
            st.markdown('Don\'t have an account?')
        
        with col2:
            if st.button("Register"):
                st.session_state.register_flg = 'register'
                st.rerun()

    if 'register_flg' in st.session_state:
        st.title('Welcome')
        with st.form("register"):
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')

            if st.form_submit_button("Register"):
                if user_register(email=email, password=password):
                    del st.session_state.register_flg
                    st.rerun()
                else:
                    st.error('Email already exists')

        col1, col2, _ = st.columns(3, vertical_alignment='center')

        with col1:
            st.markdown('Already have an account?')
        with col2:
            if st.button("Log in"):
                del st.session_state.register_flg
                st.rerun()


def profile():
    if validate_token(st.session_state.jwt_token):
        st.title("Your profile")

        user = get_user_info(user_id=st.session_state.user_id)
        user_username = user['username']
        if user['group_id'] is not None:
            if 'group_id' not in st.session_state:
                st.session_state.group_id = user['group_id']

        st.markdown(f'##### Email: {user['email']}')
        st.markdown(f'##### Username: {user_username if user_username is not None else "-"}')
        if st.button('Edit'): 
            st.session_state.edit_profile = 'edit'
            st.rerun()

        if st.sidebar.button('Log out', key="log_out"):
            del st.session_state.user_id
            del st.session_state.jwt_token
            st.rerun()

        if 'edit_profile' in st.session_state:
            st.subheader("Edit your profile:")
            with st.form("edit_profile_form"):
                username = st.text_input("Username", value=user_username)
                old_password = st.text_input("Old password", type='password')
                new_password = st.text_input("New password", type='password')

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Save changes"):
                        if edit_user(user_id=st.session_state.user_id, username=username, old_password=old_password, new_password=new_password):
                            del st.session_state.edit_profile
                            st.rerun()
                        else:
                            st.error('Something went wrong')

                with col2:
                    if st.form_submit_button("Close"):
                        del st.session_state.edit_profile
                        st.rerun()
    else:
        del st.session_state.user_id
        del st.session_state.jwt_token
        st.rerun()


def group():
    if validate_token(st.session_state.jwt_token):
        if 'group_id' in st.session_state:
            group_info = get_group_info(user_id=st.session_state.user_id)
            group_name = group_info['group_name']
            your_status = group_info['group_status']

            st.title(f"Your group: {group_name}")

            col_status, _, col_edit = st.columns(3, vertical_alignment='center')

            with col_status:
                st.markdown(f'##### Your status: {your_status}')

            if your_status == 'owner':
                with col_edit:
                    if st.button('Edit'): 
                            st.session_state.edit_group = 'edit'
                            st.rerun()

            if 'edit_group' in st.session_state:
                st.subheader("Edit your group:")
                with st.form("edit_group_form"):
                    group_name = st.text_input("Group name", value=group_name)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save changes"):
                            if edit_group(user_id=st.session_state.user_id, group_name=group_name):
                                del st.session_state.edit_group
                                st.rerun()
                            else:
                                st.error('Something went wrong')

                    with col2:
                        if st.form_submit_button("Close"):
                            del st.session_state.edit_group
                            st.rerun()

            st.divider()

            if 'add_user' in st.session_state:
                st.subheader("Add new user to your group:")
                with st.form("add_user_form"):
                    email = st.text_input("Email")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Add user"):
                            if add_member(group_id=st.session_state.group_id, email=email):
                                del st.session_state.add_user
                                st.rerun()
                            else:
                                st.error('User wasn\'t added')

                    with col2:
                        if st.form_submit_button("Close"):
                            del st.session_state.add_user
                            st.rerun()

            col1, _, col3 = st.columns(3, vertical_alignment='center')
            with col1:
                st.subheader('Group users:')
            with col3:
                if your_status == 'owner':
                    if st.button('Add user'): 
                        st.session_state.add_user = 'add'
                        st.rerun()
            
            users = view_members(group_id=st.session_state.group_id)

            if users:
                for user in users:
                    col1, col2, col3 = st.columns(3, vertical_alignment='center')
                    with col1:
                        st.markdown(f'{user[0] if user[0] is not None else ""} ({user[1]})')
                    with col2:
                        st.markdown(user[2])
                    with col3:
                        if your_status == 'owner' and user[2] != 'owner':
                            with st.popover('Delete user'): 
                                st.markdown('You really want to delete this user?')
                                if st.button('Yes'):
                                    if delete_member(user[1]):
                                        st.rerun()
                                
            else:
                st.markdown('There is no users in your group!')

        else:
            st.markdown('##### You are not in a group!')
            if 'create_group' not in st.session_state:
                if st.button('Create group'):
                    st.session_state.create_group = 'create'
                    st.rerun()
            
            if 'create_group' in st.session_state:
                st.subheader('Create a group')
                with st.form("create_group_form"):
                    group_name = st.text_input("Group name")

                    col1, col2, _, _, _ = st.columns(5)
                    with col1:
                        if st.form_submit_button("Create group"):
                            result = create_group(user_id=st.session_state.user_id, group_name=group_name)
                            if result:
                                st.session_state.group_id = result
                                del st.session_state.create_group
                                st.rerun()
                            else:
                                st.error('Something went wrong')

                    with col2:
                        if st.form_submit_button("Close"):
                            del st.session_state.create_group
                            st.rerun()

    else:
        del st.session_state.user_id
        del st.session_state.jwt_token
        st.rerun()
        

def budget_management():
    if validate_token(st.session_state.jwt_token):
        if 'group_id' in st.session_state:
            st.title("Budget management")

            if "edit_budget_id" not in st.session_state:
                st.subheader("Add new budget:")
                with st.form("add_budget_form"):
                    budget_name = st.text_input("Budget name", value='')
                    total_budget = st.number_input("Total money", min_value=0, step=1, value=0)
                    submitted = st.form_submit_button("Add")

                    if submitted:
                        if add_budget(st.session_state.group_id, budget_name, total_budget):
                            st.success("Budget was succesfully added.")
                        else:
                            st.error("Error: budget wasn't added.")

            if "edit_budget_id" in st.session_state:
                budget_id = st.session_state.edit_budget_id
                budget_name = st.session_state.edit_budget_name
                total_budget = st.session_state.edit_total_budget
                st.subheader(f"Edit budget: {budget_name}")
                with st.form("edit_budget_form"):
                    budget_name = st.text_input("Budget name", value=budget_name)
                    total_budget = st.number_input("Total budget", min_value=0, step=1, value=total_budget)
                    submitted = st.form_submit_button("Save changes")

                    if submitted:
                        if edit_budget(budget_id, budget_name, total_budget):
                            del st.session_state.edit_budget_id
                            del st.session_state.edit_budget_name
                            del st.session_state.edit_total_budget
                            st.rerun()
                        else:
                            st.error("Error: budget wasn't updated.")

            all_budgets = get_all_budgets(st.session_state.group_id)
            st.subheader("All budgets:")

            budgets = all_budgets['budgets']

            if budgets:
                for budget in budgets:
                    col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
                    with col1:
                        st.write(f"**{budget['budget_name']}** - {budget['total_budget']} UAH")
                    with col2:
                        if st.button("Edit", key=f"edit_budget_{budget['budget_id']}"):
                            st.session_state.edit_budget_id = budget['budget_id']
                            st.session_state.edit_budget_name = budget['budget_name']
                            st.session_state.edit_total_budget = budget['total_budget']
                            st.rerun()
                    with col3:
                        with st.popover("Delete budget"):
                            st.markdown('You really want to delete this budget?')
                            if st.button('Yes', key=f"delete_budget_{budget['budget_id']}"):
                                if delete_budget(budget['budget_id']):
                                    if 'current_budget' in st.session_state:
                                        del st.session_state.current_budget
                                    st.rerun()
                    with col4:
                        if st.button("View expenses", key=f"view_{budget['budget_id']}"):
                            st.session_state.current_budget = budget['budget_id']
            else:
                st.write("There is no budgets to view.")

            if "current_budget" in st.session_state:
                budget_id = st.session_state.current_budget
                
                result = get_expenses(budget_id)
                expenses = result['expenses']
                budget_of_expense = result['budget']
                total = budget_of_expense[1]
                spent_this_month = result['spent_this_month']
                spent_this_month = spent_this_month if spent_this_month is not None else 0
                categories = result['categories']
                category_dict = {category[1]: category[0] for category in categories}

                st.subheader(f"Selected budget is {budget_of_expense[0]}:")

                col_total, col_spent = st.columns(2, vertical_alignment='center')
                with col_total:
                    st.markdown(f"Total budget = {budget_of_expense[1]} UAH")
                with col_spent:
                    st.markdown(f"Spent this month = {spent_this_month} UAH")

                if "edit_expense_id" not in st.session_state:
                    st.subheader("Add new expense:")
                    with st.form("add_expense_form"):
                        expense_name = st.text_input("Expense description", value='')
                        expense_price = st.number_input("Spent money (UAH)", min_value=0, step=1, value=0)
                        expense_type = st.selectbox("Expense type", ['current', 'planned'])
                        category = st.selectbox("Category", list(category_dict.keys()))
                        submit_expense = st.form_submit_button("Add")

                        if submit_expense:
                            if expense_price + int(spent_this_month) > total and expense_type == 'current':
                                st.error('Sorry, you don\'t have enough money for this')
                            else:
                                if add_expense(budget_id, expense_name, expense_price, expense_type, category_dict[category]):
                                    st.rerun()
                                else:
                                    st.error("Error: expense wasn't added.")

                if "edit_expense_id" in st.session_state:
                    st.subheader("Edit expense:")

                    expense_id = st.session_state.edit_expense_id
                    description = st.session_state.edit_expense_description
                    price = st.session_state.edit_expense_price
                    expense_type = st.session_state.edit_expense_expense_type
                    category_id = st.session_state.edit_expense_category_id
                    
                    with st.form("edit_expense_form"):
                        expense_name = st.text_input("Expense description", value=description)
                        expense_price = st.number_input("Spent money (UAH)", min_value=0, step=1, value=price)
                        expense_type = st.selectbox("Expense type", ['current', 'planned'], index=0 if expense_type == 'current' else 1)
                        category = st.selectbox("Category", list(category_dict.keys()), index=category_id-1)
                        submit_expense = st.form_submit_button("Save changes")

                        if submit_expense:
                            if expense_price + int(spent_this_month) > total and expense_type == 'current':
                                st.error('Sorry, you don\'t have enough money for this')
                            else:
                                if edit_expense(expense_id, expense_name, expense_price, expense_type, category_dict[category]):
                                    del st.session_state.edit_expense_id
                                    del st.session_state.edit_expense_description
                                    del st.session_state.edit_expense_price
                                    del st.session_state.edit_expense_expense_type
                                    del st.session_state.edit_expense_category_id
                                    st.rerun()
                                else:
                                    st.error("Error: expense wasn't updated.")

                st.markdown(f"#### All expenses:")

                if expenses:
                    for expense in expenses:
                        col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='center')
                        with col1:
                            st.write(f"**{expense['description']}** - {expense['price']} UAH - {expense['expense_type']}")
                        with col2:
                            for id, name in categories:
                                if id == expense['category_id']:
                                    st.write(f"{name}")
                                    break
                        with col3:
                            st.write(f"{datetime.strptime(expense['created_date'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y')}")
                        with col4:
                            if st.button("Edit", key=f"edit_expense_{expense['expense_id']}"):
                                st.session_state.edit_expense_id = expense['expense_id']
                                st.session_state.edit_expense_description = expense['description']
                                st.session_state.edit_expense_price = expense['price']
                                st.session_state.edit_expense_expense_type = expense['expense_type']
                                st.session_state.edit_expense_category_id = expense['category_id']
                                st.rerun()
                        with col5:
                            with st.popover("Delete"):
                                st.markdown('You really want to delete this expense?')
                                if st.button('Yes', key=f"delete_expense_{expense['expense_id']}"):
                                    if delete_expense(expense['expense_id']):
                                        st.rerun()
                else:
                    st.write("There is no expenses to view.")

                if st.button('Close expenses'):
                    del st.session_state.current_budget
                    st.rerun()

        else:
            st.markdown('##### You are not in a group!')

    else:
        del st.session_state.user_id
        del st.session_state.jwt_token
        st.rerun()


def purchase_planning():
    if validate_token(st.session_state.jwt_token):
        if 'group_id' in st.session_state:
            st.title("Purchase planning")

            st.subheader("Add shopping list:")
            with st.form("add_list_form"):
                name = st.text_input("Shipping list name", value='')
                balance = st.number_input("Money", min_value=0, step=1, value=0)
                submitted = st.form_submit_button("Add")

                if submitted:
                    if add_list(st.session_state.user_id, name, balance):
                        st.success("List was succesfully added.")
                    else:
                        st.error("Error: list wasn't added.")

            st.subheader('Shopping lists:')
            lists = view_shopping_lists(user_id=st.session_state.user_id)

            if lists:
                for lst in lists:
                    col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
                    with col1:
                        st.write(f"**{lst['name']}**")
                    with col2:
                        st.write(f'{lst['balance']} UAH')
                    with col3:
                        with st.popover("Delete"):
                            st.markdown('You really want to delete this list?')
                            if st.button('Yes', key=f"delete_list_{lst['list_id']}"):
                                if delete_list(list_id=lst['list_id'], user_id=st.session_state.user_id):
                                    if 'current_list' in st.session_state:
                                        del st.session_state.current_list
                                    st.rerun()
                    with col4:
                        if st.button("View items", key=f"view_{lst['list_id']}"):
                            st.session_state.current_list = lst['list_id']
                            st.session_state.current_list_name = lst['name']
                            st.session_state.current_list_balance = lst['balance']

                if 'current_list' in st.session_state:
                    st.divider()

                    if 'add_item' in st.session_state:
                        propose = get_propositions(user_id=st.session_state.user_id)
                        st.markdown("#### Add new item:")

                        col_form, col_propose = st.columns(2)
                        with col_form:
                            with st.form("add_item_form"):
                                name = st.text_input("Item name", value='')
                                description = st.text_input("Description", value='')
                                add_info = st.text_input("Additional info", value='')
                                price = st.number_input("Price", min_value=0, step=1, value=0)

                                col_add, _, _, col_close = st.columns(4)
                                with col_add:
                                    submitted = st.form_submit_button("Add")
                                with col_close:
                                    if st.form_submit_button('Close'):
                                        del st.session_state.add_item
                                        st.rerun()

                                if submitted:
                                    if int(st.session_state.current_list_balance) - price < 0:
                                        st.error('Sorry, you don\'t have enough money')
                                    else:
                                        if add_item(user_id=st.session_state.user_id, name=name, price=price, list_id=st.session_state.current_list, description=description, add_info=add_info):
                                            del st.session_state.add_item
                                            st.rerun()
                                        else:
                                            st.error("Error: item wasn't added.")

                        with col_propose:
                            st.markdown('##### Propositions:')
                            for propos in propose:
                                st.markdown(f'- {propos["text"]}')

                    st.subheader(f'Selected list is {st.session_state.current_list_name}')
                    st.markdown(f'##### Current balance = {st.session_state.current_list_balance}')
                    if st.button('Add new item'):
                        st.session_state.add_item = 'add'
                        st.rerun()

                    items = view_items(list_id=st.session_state.current_list, user_id=st.session_state.user_id)

                    if items:
                        for item in items:
                            col1, col2, col3 = st.columns(3, vertical_alignment='center')

                            with col1:
                                st.markdown(f'{item["name"]} - {item["price"]} UAH')
                            with col2:
                                st.markdown(f'{item["description"]}')
                            with col3:
                                if st.button("Delete", key=f"delete_item_{item['item_id']}"):
                                    if delete_item(list_id=st.session_state.current_list, user_id=st.session_state.user_id, item_id=item['item_id']):
                                        st.rerun()

                    else:
                        st.markdown('There is no items in shopping list.')

                    if st.button('Close'):
                        del st.session_state.current_list
                        if 'add_item' in st.session_state:
                            del st.session_state.add_item
                        st.rerun()
            else:
                st.markdown('There is no shopping lists to view.')

        else:
            st.markdown('##### You are not in a group!')

    else: 
        del st.session_state.user_id
        del st.session_state.jwt_token
        st.rerun()


def analytics():
    if validate_token(st.session_state.jwt_token):
        if 'group_id' in st.session_state:
            st.title("Analytics")
            expenses = get_expenses_by_group(group_id=st.session_state.group_id)
            if expenses:
                df_expenses = pd.DataFrame(expenses)
                df_expenses['created_date'] = df_expenses['created_date'].apply(lambda x: datetime.strptime(x, '%a, %d %b %Y %H:%M:%S %Z').strftime('%d/%m/%Y'))
                df_expenses['created_date'] = pd.to_datetime(df_expenses['created_date'], format='%d/%m/%Y')

                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input('Start Date', value=datetime.today().replace(day=1).date(), format='DD/MM/YYYY')
                with col_end:
                    end_date = st.date_input('End Date', format='DD/MM/YYYY')

                if start_date > end_date:
                    st.error('Start date can\'t be later than end date')

                else:
                    filtered_data = df_expenses.query("created_date >= @start_date and created_date <= @end_date")

                    col1, col2 = st.columns(2, vertical_alignment='center')
                    with col1:
                        category_chart = px.pie(
                            filtered_data,
                            names='category_name',
                            values='price',
                            title='expenses by category'
                        )
                        st.plotly_chart(category_chart)

                    with col2:
                        bar_chart = px.bar(
                            filtered_data,
                            x='created_date',
                            y='price',
                            color='category_name',
                            title='expenses by date'
                        )
                        st.plotly_chart(bar_chart)

                st.divider()

                col_text, _, col_btn = st.columns(3, vertical_alignment='center')
                with col_text:
                    st.subheader('Reports')
                if 'create_report' not in st.session_state:
                    with col_btn:
                        if st.button('Create report'):
                            st.session_state.create_report = 'create'
                            st.rerun()

                if 'create_report' in st.session_state:
                    with st.form("create_report_form"):
                        start_date_create = st.date_input('Start Date', value=datetime.today().replace(day=1).date(), format='DD/MM/YYYY')
                        end_date_create = st.date_input('End Date', format='DD/MM/YYYY')

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Create report"):
                                if start_date > end_date:
                                    st.error('Start date can\'t be later than end date')
                                else:
                                    filtered_data_create = df_expenses.query("created_date >= @start_date_create and created_date <= @end_date_create")
                                    total_expenses = filtered_data_create['price'].sum()
                                    avg_expense = filtered_data_create['price'].mean()
                                    expenses_by_category = (
                                        filtered_data_create.groupby('category_name')['price']
                                        .sum()
                                        .reset_index()
                                        .to_dict(orient='records')
                                    )
                                    if create_report(group_id=st.session_state.group_id, start_date=start_date_create, end_date=end_date_create, total=total_expenses, mean=avg_expense, by_category=expenses_by_category):
                                        del st.session_state.create_report
                                        st.rerun()
                                    else:
                                        st.error('Something went wrong')

                        with col2:
                            if st.form_submit_button("Close"):
                                del st.session_state.create_report
                                st.rerun()

                reports = get_reports_by_group(group_id=st.session_state.group_id)
                
                if reports:
                    for report in reports:
                        col1, _, col2 = st.columns(3, vertical_alignment='center')
                        with col1:
                            st.markdown(f'{report['created_date']} report')
                        with col2:
                            if st.button('Show report info', key=f'report_info{report["report_id"]}'):
                                st.session_state.report_id = report['report_id']
                                st.rerun()

                    if 'report_id' in st.session_state:
                        st.divider()
                        report = get_report_by_id(st.session_state.report_id)
                        report_data = json.loads(report['report_data'])

                        st.subheader(f'{report["created_date"]} report')

                        col_total_avg, col_category = st.columns(2)

                        with col_total_avg:
                            st.markdown(f'Start date: {report_data['start_date']}')
                            st.markdown(f'End date: {report_data['end_date']}')
                            st.markdown(f'Total expenses: {report_data['total']} UAH')
                            st.markdown(f'Avg expenses: {report_data['mean']} UAH')
                            if st.button('Close report'):
                                del st.session_state.report_id
                                st.rerun()
                        with col_category:
                            st.write(pd.DataFrame(report_data['by_category']))
                        

                else:
                    st.markdown('There is no reports!')

            else:
                st.markdown('There is no expenses!')
        else:
            st.markdown('##### You are not in a group!')

    else:
        del st.session_state.user_id
        del st.session_state.jwt_token
        st.rerun()


def main():
    if 'user_id' not in st.session_state:
        login()

    else:
        pages_names_dict = {
            "Profile": profile,
            "Group": group,
            "Budget management": budget_management,
            "Purchase planning": purchase_planning,
            "Analytics": analytics,
        }

        selected_page = st.sidebar.selectbox("Choose page:", pages_names_dict.keys())
        pages_names_dict[selected_page]()


if __name__ == "__main__":
    main()