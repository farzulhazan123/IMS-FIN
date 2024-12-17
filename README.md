 Investment Management System
 Description:
 Website Overview

This website comprises a total of 13 webpages, dedicated to monitoring personal investments in diverse assets such as stocks, mutual funds, real estate, fixed deposit, gold, and cryptocurrency. Users can also log financial activities, including income, expenses, and liabilities. The homepage prominently displays the calculated net worth. The website is developed using Flask, HTML, and CSS.


 Login Page

Upon entering the site, users are directed to the login page, where they must input their credentials (username and password) to access and monitor their investments. A side navigation bar facilitates seamless movement between the login and register pages. The login page includes links for password recovery and account creation. In the event of a forgotten password, users can click the "Forget Password?" button, leading them to a page where they provide their first and last names, along with their username. Successful verification prompts the system to process and complete the password change request. Opting to create an account redirects the user to the register webpage.


Register Page

The Register page allows users to establish a new account by entering their first and last names for identity verification in case of a forgotten password. Additionally, users are prompted to set a unique username and password. The system checks for existing usernames, displaying a message stating 'Username already exists' if necessary. Once all credentials are validated and stored, users are automatically signed in to the homepage, and their information is securely saved in the SQL database.


Homepage

The homepage is designed to offer users a centralized hub for navigating various sections of the website, providing essential information at a glance.

 Navigation Bar

Situated on the left side of the homepage is a streamlined navigation bar. It encompasses the website's logo and links to key sections, ensuring effortless navigation for users. These links include direct access to the home page, the income and expense page, and all other relevant sections of the website. At the top right corner, a profile picture serves as a convenient gateway for users to log out of the website upon clicking. Positioned directly beneath the profile picture and page name is the dynamically calculated net worth of the user. This net worth is derived by aggregating all investments and subtracting liabilities, offering a quick link to the income and expense page for further exploration.

 Body of the Homepage
 Net Worth Display

The user's net worth is dynamically calculated and prominently displayed beneath the profile picture. This real-time figure serves as a valuable indicator for users, instantly conveying their financial standing.


 Investment Breakdown

- Dynamic Pie Chart: Positioned prominently on the right side of the homepage, a dynamic pie chart aids users in visually comprehending the breakdown of their investments. This visual representation enhances user experience by providing an intuitive overview.

- Investment Listing: On the left side of the homepage, users can conveniently review all entered investments. Each investment entry serves as a clickable link, redirecting users to its respective investment page for detailed and comprehensive information.

The homepage is thoughtfully crafted to offer a user-friendly experience, combining essential navigation elements with insightful visualizations of financial data.
Income & Expense Page

This page serves as a comprehensive tool for users to track both their income and monthly expenses. The layout is divided into two distinct sections: one dedicated to income and the other to expenses, positioned opposite each other for clarity.

Income Section

At the top of the income section, the total monthly income is prominently displayed, calculated by summing the user-inputted income. Directly below, a user-friendly form allows users to input their income details. This form comprises a dropdown menu featuring various income types such as Post Tax Salary, Business Income, Rental Income, and more. Users can then specify the income amount and seamlessly add it to the database.

Following the 'Add' button, a table is presented, showcasing all recorded income sources. Users have the flexibility to edit or delete entries within this table. Opting to edit redirects users to a dedicated page where they can input the new amount, save it to the database, and subsequently return to the Income and Expense page. Alternatively, selecting the delete option triggers an automatic page refresh, removing the chosen income entry from the table.

Expense Section

The expense section mirrors the style and process of the income section. It incorporates dropdown options like Monthly Expense, Loan EMI, Insurance Premiums, and others, enabling users to categorize their expenses efficiently.

The page structure ensures a seamless and intuitive experience for users to manage both their income and expenses effectively.
Liabilities Page

The hero section contains a "Total Value" display, showcasing the cumulative value of liabilities added by the user. On the right side of the hero section, an "Add" button is prominently featured. Clicking this button redirects the user to the "Add Liabilities" page, where details for new liabilities can be entered. Just below the hero section, a table is presented to provide a comprehensive view of all the liabilities added by the user.

The table consists of five columns:

1. Number: Sequential numbering for each liability.
2. Name: The name or title associated with the liability.
3. Value: The monetary value of the liability.
4. Edit: An input button allowing users to modify the existing value of the liability.
5. Delete: A delete button for removing the liability from the table.
Add Liabilities Page

This page features two input fields—one for entering the title and the other for specifying the value of the liability. Additionally, a "Save" button is provided to confirm and add the liability to the table. Upon saving, the user is automatically redirected to the liabilities page, where the updated table reflects the newly added liability.
Stocks Page

Similar to the Liabilities page, the Stocks page features a table where users can monitor their stock investments. The table comprises the following columns:

1. Number: Sequential numbering for each stock entry.
2. Name: The name of the stock.
3. Type: Classification of the stock, such as Small Cap, Mid Cap, Large Cap, etc.
4. Quantity: The number of shares owned.
5. Price per Share: The price of one share.
6. Total Value: Calculated by multiplying the quantity of shares and the price per share.
7. Delete: A delete button for removing the stock entry from the table.

Clicking the "Add" button redirects users to the Add Stock page.
Add Stock Page

The Add Stock page consists of a user-friendly form with the following input fields:

1. Stock Name: Enter the name of the stock.
2. Quantity: Specify the quantity of shares.
3. Price per Share: Input the price of one share.
4. Type: A dropdown button to choose the classification of the stock, including options like Large Cap, Mid Cap, Small Cap, or Others.
5. Save: A button to confirm and add the stock data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

- Type (Classification): The dropdown selection is verified at the backend to ensure correct input.

Upon successful validation, clicking the Save button adds the stock data, providing users with a seamless experience in managing their stock investments.
Mutual Funds Page

Similar to the Liabilities page, the Mutual Funds page features a table where users can monitor their mutual fund investments. The table comprises the following columns:

1.Number: Sequential numbering for each mutual fund entry.
2.Name: The name of the mutual funds
3.Quantity: The number of shares owned.
4.Price per Share: The price of one share.
5.Total Value: Calculated by multiplying the quantity and the price per share.
6.Delete: A delete button for removing the mutual fund entry from the table.

Clicking the "Add" button redirects users to the Add Mutual fund page.
Add Mutual fund Page

The Add Mutual funds page consists of a user-friendly form with the following input fields:

1.Mutual funds Name: Enter the name of the mutual fund.
2.Quantity: Specify the quantity of shares.
3.Price per Share: Input the price of one share.
4.Save: A button to confirm and add the mutual fund data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

Upon successful validation, clicking the Save button adds the mutual funds data, providing users with a seamless experience in managing their mutual funds’ investments.
Real Estate Page

Similar to the Liabilities page, the Real estates page features a table where users can monitor their Real estate investments. The table comprises the following columns:

1.Number: Sequential numbering for each Real estate entry.
2.Title: The title of the Real estate.
3.Type: Classification of the Real estate, such as Commercial Real Estate, REITs, Fractional Ownership, Others.
4.Value: Value of the real estate added.
5.Delete: A delete button for removing the Real estate entry from the table.

Clicking the "Add" button redirects users to the Add Real estate page.

Add Real Estate Page

The Add Real estate page consists of a user-friendly form with the following input fields:

1.Real estate Title: Enter the title of the Real estate.
2.Value: Input the total value of real estate.
3.Type: A dropdown button to choose the classification of the Real estate, including options like Commercial Real Estate, REITs, Fractional Ownership, Others.
4.Save: A button to confirm and add the Real estate data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

- Type: The dropdown selection is verified at the backend to ensure correct input.

Upon successful validation, clicking the Save button adds the Real estate data, providing users with a seamless experience in managing their Real estate investments.
Fixed Deposit Page

The Fixed Deposit page features a table where users can monitor their Fixed Deposit investments. The table comprises the following columns:

1.Number: Sequential numbering for each Fixed Deposit entry.
2.Title: The title of the Fixed Deposit investments.
3.Tenure:The time period of the Fixed Deposit
4.Value: Value of Fixed Deposit investment.
5.Delete: A delete button for removing the Fixed Deposit entry from the table.

Clicking the Add button redirects users to the Add Fixed Deposit page.

Add Fixed Deposit Page

The Add Fixed Deposit page consists of a user-friendly form with the following input fields:

1.Fixed Deposit Name: Enter the name of the Fixed Deposit.
2.Tenure: A dropdown button to choose the tenure of the Fixed Deposit.
3.Value: Enter the Value of Fixed Deposit investment.
4.Save: A button to confirm and add the Fixed Deposit data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

- Type (Classification): The dropdown selection is verified at the backend to ensure correct input.

Upon successful validation, clicking the Save button adds the Fixed Deposit investment data, providing users with a seamless experience in managing their Fixed Deposit investments.
Gold investment Page

Similar to the Liabilities page, the Gold investment page features a table where users can monitor their Gold investments. The table comprises the following columns:

1.Number: Sequential numbering for each Gold entry.
2.Title: The title for the Gold.
3.Type: Classification of the Gold, such as SGB ,  Physical Gold ,  Digital Gold ,  Others.
4.Value: Total Value of gold.
5.Delete: A delete button for removing the Gold entry from the table.

Clicking the Add button redirects users to the Add Gold page.

Add Gold Page

The Add Gold page consists of a user-friendly form with the following input fields:

1.Gold Name: Enter the name of the Gold investment.
2.Type: A dropdown button to choose the classification of the Gold, including options like SGB ,  Physical Gold ,  Digital Gold ,  Others.
3.Value: Enter Total Value of gold.
4.Save: A button to confirm and add the Gold data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

- Type (Classification): The dropdown selection is verified at the backend to ensure correct input.

Upon successful validation, clicking the Save button adds the Gold data, providing users with a seamless experience in managing their Gold investments.
Crypto Page

Similar to the Liabilities page, the Cryptos page features a table where users can monitor their Crypto investments. The table comprises the following columns:

1.Number: Sequential numbering for each Crypto entry.
2.Name: The name of the Crypto investment.
3.Quantity: The number of crypto owned.
4.Price per coin: The price of one coin.
5.Total Value: Calculated by multiplying the quantity of coins and the price per coin.
6.Delete: A delete button for removing the Crypto coin entry from the table.

Clicking the "Add" button redirects users to the Add Crypto page.

Add Crypto Page

The Add Crypto page consists of a user-friendly form with the following input fields:

1.Crypto Coin Name: Enter the name of the Crypto coin.
2.Quantity: Specify the quantity of coins.
3.Price: Input the price of one coin.
4.Save: A button to confirm and add the Crypto coin to data.

Validation and verification processes are implemented for each input:

- Name, Quantity, and Price: These fields are validated to ensure they are not missing and contain correct data. If any data is incorrect or missing, users are prompted to re-enter the information with the correct data.

Upon successful validation, clicking the Save button adds the Crypto coin data, providing users with a seamless experience in managing their Crypto investments.


