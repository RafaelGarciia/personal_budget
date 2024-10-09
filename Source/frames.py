import tkinter as tk
import tkinter.ttk as ttk
from Source.window import Window
import Source.utils as utl
import Source.sql as sql


class Pattern_screen(tk.Frame):
    def __init__(self, root: Window):
        super().__init__(
            master=root,
            width=root.width,
            height=root.height,
            bg='lightgray',
        )


class BudGet_screen(Pattern_screen):
    def __init__(self, root):
        super().__init__(root)

        # Starting the Frames
        insert_frame = tk.Frame(self, relief='ridge', bd=1)
        table_frame = tk.Frame(self, height=200, width=200)
        description_frame = tk.Frame(insert_frame, height=200, width=200)
        date_frame = tk.Frame(insert_frame, height=200, width=200)
        value_frame = tk.Frame(insert_frame, height=200, width=200)
        buttons_frame = tk.Frame(insert_frame, height=200, width=200)

        # Modeling the description frame
        tk.Label(description_frame, text='Desc.').pack(
            anchor='nw', expand=False, side='left'
        )
        self.desc_entry = tk.Entry(description_frame, width=30)
        self.desc_entry.pack(anchor='nw', expand=False, padx=5, side='left')

        # Modeling the date frame
        tk.Label(date_frame, text='Date').pack(
            anchor='nw', expand=False, side='left'
        )
        self.day_entry = tk.Entry(date_frame, justify='center', width=3)
        self.day_entry.pack(anchor='nw', expand=False, padx=9, side='left')
        self.month_combobox = ttk.Combobox(
            date_frame,
            justify='center',
            values=[i + 1 for i in range(12)],
            width=3,
        )
        self.month_combobox.pack(anchor='nw', expand=False, side='left')
        filter_icon = tk.PhotoImage(
            file='Source\\icons\\config.png'
        ).subsample(4, 4)
        filter_button = tk.Button(
            date_frame,
            image=filter_icon,
            relief='flat',
            command=self.load_treeview,
        )
        filter_button.image = filter_icon
        filter_button.pack(anchor='nw', expand=False, padx=5, side='top')

        # Modeling the value frame
        tk.Label(value_frame, text='Value').grid(column=1, row=0)
        self.value_entry = tk.Entry(value_frame, justify='center', width=7)
        self.value_entry.grid(column=1, row=1)
        tk.Label(value_frame, text='R$').grid(column=0, row=1)

        # Modeling the buttons frame
        insert_icon = tk.PhotoImage(
            file='Source\\icons\\insert.png'
        ).subsample(4, 4)
        insert_button = tk.Button(
            buttons_frame,
            image=insert_icon,
            relief='flat',
            command=self.insert_release,
        )
        insert_button.image = insert_icon
        insert_button.pack(padx=2, pady=2, side='top')
        delete_icon = tk.PhotoImage(
            file='Source\\icons\\delete.png'
        ).subsample(4, 4)
        delete_button = tk.Button(
            buttons_frame, image=delete_icon, relief='flat', command=...
        )
        delete_button.image = delete_icon
        delete_button.pack(padx=2, pady=2, side='top')

        # Modeling the table treeview frame
        self.table_treeview = ttk.Treeview(
            table_frame,
            columns=('id', 'day', 'desc', 'value', 'bal'),
            show='headings',
        )
        self.table_treeview.place(x=5, y=5, width=593, height=380)
        self.table_treeview.bind(
            '<Double-Button-1>', self.select_item_in_treeview
        )
        table_scrollbar = tk.Scrollbar(table_frame, orient='vertical')
        table_scrollbar.pack(fill='y', side='right', padx=5, pady=5)
        self.table_treeview.heading('id', text='Id')
        self.table_treeview.heading('day', text='Day')
        self.table_treeview.heading('desc', text='Description')
        self.table_treeview.heading('value', text='Value')
        self.table_treeview.heading('bal', text='Balance')
        self.table_treeview.column('id', width=0)
        self.table_treeview.column('day', width=15, anchor='center')
        self.table_treeview.column('desc', width=300, anchor='w')
        self.table_treeview.column('value', width=100, anchor='w')
        self.table_treeview.column('bal', width=100, anchor='w')
        self.table_treeview.configure(yscroll=table_scrollbar.set)

        # Insert the current month into the widget
        self.month_combobox.insert(0, utl.get_month_today())

        # Place the frames
        insert_frame.place(anchor='nw', height=60, width=620, x=10, y=10)
        table_frame.place(anchor='nw', height=390, width=620, x=10, y=80)
        description_frame.place(anchor='nw', x=5, y=5)
        date_frame.place(anchor='nw', x=5, y=30)
        value_frame.place(anchor='nw', x=230, y=7)
        buttons_frame.pack(expand=False, fill='y', side='right')

        self.load_treeview()

    def load_treeview(self):
        month_filter = self.month_combobox.get()
        # Table control variable
        self.id = None

        # Clean treeview
        self.table_treeview.delete(*self.table_treeview.get_children())

        # Request to the database
        connection, cursor = sql.connect()
        query = cursor.execute(
            """
            SELECT id, day, month, desc, value FROM releases
            WHERE month = '%s' ORDER BY day ASC;
        """
            % month_filter
        )

        # Calculating the balance
        balance = 0
        for item in query:
            value = float(str(item[4]).replace(',', '.'))
            balance = float(balance) + value
            insert_values = [
                item[0],
                item[1],
                item[3],
                f'R$ - {utl.to_money( value ).replace('-', ' ')}'
                if value < 0
                else f'R$   {utl.to_money( value )}',
                f'R$ - {utl.to_money(balance).replace('-', ' ')}'
                if balance < 0
                else f'R$   {utl.to_money(balance)}',
            ]
            self.table_treeview.insert('', tk.END, values=insert_values)

        # Finishing request
        connection.close()

    def insert_release(self):

        # Collects information entered by the user
        return_entries = []
        for entry in [
            self.day_entry,
            self.desc_entry,
            self.value_entry,
            self.month_combobox,
        ]:
            return_entries.append(entry.get())

        # Request to the database
        connection, cursor = sql.connect()
        # If the information is new, insert it into the database.
        # else, if you edit a record, update the record.
        if self.id == None:
            cursor.execute(
                """INSERT INTO releases (day, desc, value, month) VALUES ( ?, ?, ?, ? )""",
                return_entries,
            )
        else:
            return_entries.append(self.id)
            cursor.execute(
                """UPDATE releases SET day=?, desc=?, value=?, month=? WHERE id=?;""",
                return_entries,
            )

        # Finishing request
        connection.commit()
        connection.close()

        # Clear entrys
        for entry in [self.day_entry, self.desc_entry, self.value_entry]:
            entry.delete(0, tk.END)

        # Reload treeview
        self.load_treeview()

    def select_item_in_treeview(self, event):

        # Get the item that is selected
        select_item = self.table_treeview.item(
            self.table_treeview.selection()[0], 'values'
        )

        # Clear entrys
        for entry in [
            self.day_entry,
            self.desc_entry,
            self.value_entry,
            self.month_combobox,
        ]:
            entry.delete(0, tk.END)

        # Request to the database
        connection, cursor = sql.connect()
        query = cursor.execute(
            """
            SELECT id, day, month, desc, value FROM releases
            WHERE id = '%s' ORDER BY day ASC;           
        """
            % select_item[0]
        )

        # Collecting and separating request records
        records = []
        for record in query:
            for item in record:
                records.append(item)

        self.id = records[0]
        self.day_entry.insert(0, records[1])
        self.month_combobox.insert(0, records[2])
        self.desc_entry.insert(0, records[3])
        self.value_entry.insert(0, records[4])

        # Finishing request
        connection.close()
