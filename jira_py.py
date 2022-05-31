from jira import JIRA
import tkinter as tk
from fillpdf import fillpdfs
import tempfile


jira = JIRA("https://westmedwa.atlassian.net", basic_auth=("joshua@westmedwa.com","api-key"))
master = tk.Tk()
master.title("PyJira")

tsc = jira.attachment(11304)

tsc_file = tsc.get()

with open("tsc.pdf",'wb') as f:
    f.write(tsc_file)
#pdf_template = current_dir + "/TSC_pyfiller.pdf"

pdf_template = "tsc.pdf"



p1 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=1)
p2 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=2)
p3 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=3)
p4 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=4)


def onClick():
    global issues
    issues = str(e1.get())
    master.quit()


tk.Label(master, text="Enter JQL query").grid(row=0)


e1 = tk.Entry(master)

e1.grid(row=0, column=1)

tk.Button(master,text='Enter', command = onClick ).grid(row=3,column=1,sticky=tk.W,pady=4)


tk.mainloop()

print("JQL query: " + "\"" + issues + "\"")



for issue in jira.search_issues(issues):
    key = issue.key

    if 'RPH' in key:

        assignee = issue.fields.assignee.displayName
        initals = ''.join([x[0].upper() for x in assignee.split(' ')])
        s_n = issue.fields.customfield_10166
        p_2 = issue.fields.customfield_10173
        p_5 = issue.fields.customfield_10174
        p_9 = issue.fields.customfield_10175
        pmax = issue.fields.customfield_10176
        pmin = issue.fields.customfield_10177
        pdoor = issue.fields.customfield_10178
        acc = issue.fields.customfield_10179
        airval = issue.fields.customfield_10182
        hsp = issue.fields.customfield_10183.value
        waterval = issue.fields.customfield_10188

        tsc_date = issue.fields.customfield_10015
        update_date = issue.fields.updated[:10]
        update_date_2 = str(int(tsc_date[:4])+2) + '-' + tsc_date[5:]

    elif 'SCGH' in key:
        assignee = issue.fields.assignee.displayName
        initals = ''.join([x[0].upper() for x in assignee.split(' ')])
        s_n = issue.fields.customfield_10187
        p_2 = issue.fields.customfield_10156
        p_5 = issue.fields.customfield_10157
        p_9 = issue.fields.customfield_10184
        pmax = issue.fields.customfield_10158
        pmin = issue.fields.customfield_10159
        pdoor = issue.fields.customfield_10160
        acc = issue.fields.customfield_10161
        airval = issue.fields.customfield_10163
        hsp = issue.fields.customfield_10186.value
        waterval = issue.fields.customfield_10194

        tsc_date = issue.fields.customfield_10193
        update_date = issue.fields.updated[:10]
        update_date_2 = str(int(tsc_date[:4])+2) + '-' + tsc_date[5:]


    p1.update({'Textfield':hsp,'Serial No':s_n,'Equipment No':key,})

    p2.update({'Textfield-3':p_2,'Textfield-4':p_5,'Textfield-5':p_9,'Textfield-6':pmin,'Pmax 18  25 bar-0':pmax,'Textfield-7':pdoor,'Textfield-8':acc})

    p3.update({'Water value 600 mV-0':waterval,'Textfield-11':'0','Air value  100 mV-0':airval})

    p4.update({'Test result Defects found which could endanger pat':'Off','Textfield-16':assignee,'Textfield-17':initals,'Textfield-18':tsc_date,'Textfield-19':update_date_2,'Textfield-20':'Buffer'})

    p2.update(p1)
    p3.update(p2)
    p4.update(p3)

    fillpdfs.write_fillable_pdf(pdf_template,key+'.pdf', p4)
    fillpdfs.flatten_pdf(key+'.pdf', key+'.pdf', as_images=False)
    jira.add_attachment(issue=issue, attachment= key+'.pdf')
