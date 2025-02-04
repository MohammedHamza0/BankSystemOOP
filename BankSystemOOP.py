import streamlit as st

class BalanceException(Exception):
    pass

class BankAcount:
    users = {}
    def __init__(self, initial_balance, account_name, password):
        self.balance = initial_balance
        self.name = account_name
        self.password = password
        BankAcount.users[self.name] = {"Name": self.name, 
                                       "Balance": self.balance,
                                       "Password": self.password}
        
    def UserInfo(self):
        st.info(f"Name: '{self.name}', Balance: '${self.balance}' and Password: '{self.password}'", icon="💬")
        
    def Deposit(self, amount):
        self.balance += amount   
        
    def AvilableBalance(self, amount):
        if self.balance >= amount:
            return
        else:
            st.warning("You don't have enough balance..")
            raise BalanceException("Not enough balance")
            
    def Withdraw(self, amount):
        try:
            self.AvilableBalance(amount)
            self.balance -= amount
            
            
        except BalanceException as error:
            st.error(f"Interrupted Process...❌, {error}. Your balance = ${self.balance}")
            
    def transfer(self, amount, target_account):
        try:
            self.Withdraw(amount)
            target_account.Deposit(amount)
            
        except BalanceException:
            st.error("Transfer failed due to insufficient funds.")

def main():
    st.header("Bank Management System..🏦")
    page = st.sidebar.selectbox("Select The Process..", 
                                ["Create a New User", "User Info", "Deposit", "Withdraw", "Transfer", "Delete a user"])
    
    if "User" not in st.session_state:
        st.session_state.User = {}
    
    if page == "Create a New User":
        st.subheader("New User department.", divider='rainbow')
        UserName = st.text_input("Enter the user name")
        UserPassword = st.text_input("Enter the user password", type="password")
        UserBalance = st.number_input("Enter the user balance", min_value=0.0)
        if st.button("Create a user"):
            if (len(UserName)>= 3  and len(UserPassword)>= 3):
                UserAccount = BankAcount(UserBalance, UserName, UserPassword)
                st.session_state.User[UserName] = UserAccount
                st.success("The user created.")
            else:
                st.warning("rewrite a correct name and password, at least 3 characters", icon="✍")
                
    elif page == "User Info":
        st.subheader("User Info department.", divider='rainbow')
        if st.session_state.User:
            UserChoose = st.selectbox("Choose the user", list(st.session_state.User.keys()))
            if st.button("User info"):
                st.session_state.User[UserChoose].UserInfo()
        else:
            st.warning("No users available.")
    
    elif page == "Deposit":
        st.subheader("Deposit department.", divider='rainbow')
        if st.session_state.User:
            UserChoose = st.selectbox("Choose the user", list(st.session_state.User.keys()))
            DepositAmount = st.number_input("Enter the deposit amount", min_value=0.0)
            UserPassword = st.text_input("Enter the user password", type="password")
            if st.button("Deposit"):
                if UserPassword == st.session_state.User[UserChoose].password:
                    st.session_state.User[UserChoose].Deposit(DepositAmount)
                    st.success("Transaction completed.")
                else:
                    st.error("Wrong password..❌")
        else:
            st.warning("No users available.")
                        
    elif page == "Withdraw":
        st.subheader("Withdraw department.", divider='rainbow')
        if st.session_state.User:
            UserChoose = st.selectbox("Choose the user", list(st.session_state.User.keys()))
            WithdrawAmount = st.number_input("Enter the withdraw amount", min_value=0.0)
            UserPassword = st.text_input("Enter the user password", type="password")
            if st.button("Withdraw"):
                if UserPassword == st.session_state.User[UserChoose].password:
                    st.session_state.User[UserChoose].Withdraw(WithdrawAmount)
                    st.success("Withdraw completed..✅")
                    
                else:
                    st.error("Wrong password..❌")
        else:   
            st.warning("No users available.")
            
    elif page == "Transfer":
        st.subheader("Transfer department", divider="rainbow")
        if len(st.session_state.User.keys()) >= 2:
            SenderUser = st.selectbox("Choose the sender user", list(st.session_state.User.keys()))
            ReciverUser = st.selectbox("Choose the receiver user", 
                                    [user for user in st.session_state.User.keys() if user != SenderUser])

            TransferAmount = st.number_input("Enter the transfer amount", min_value=0.01) 
            UserPassword = st.text_input("Enter the user password", type="password") 
            if st.button("Transfer"):
                if UserPassword == st.session_state.User[SenderUser].password:
                    if SenderUser != ReciverUser:  
                        prev_balance = st.session_state.User[ReciverUser].balance
                        try:
                            st.session_state.User[SenderUser].transfer(TransferAmount, st.session_state.User[ReciverUser])
                            new_balance = st.session_state.User[ReciverUser].balance
                            if float(new_balance) > float(prev_balance):
                                st.success("Transaction complete..✅")
                        except BalanceException:
                            st.error("Transfer failed due to insufficient funds.")
                    else:
                        st.warning("Sender and receiver cannot be the same user.") 
                else:
                    st.error("Wrong password..❌")       
        else:
            st.warning("At least two users are required to perform a transfer.")
        
    elif page == "Delete a user":
        if len(st.session_state.User.keys()) >= 1:
            DeletedUser = st.selectbox("Choose a user to delete", list(st.session_state.User.keys()))
            if st.button("Delete"):
                del st.session_state.User[DeletedUser]
                st.success(f"The user '{DeletedUser}' deleted..")
        else:
            st.warning("There are no users to delete")


            
            
    st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.info("Created By: Mohammed Hamza", icon="🔥") 

if __name__ == "__main__":
    main()
