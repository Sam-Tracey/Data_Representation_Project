from dataDAO import dataDAO
import pandas as pd
#dataDAO.loadMFGEMP()
#dataDAO.loadOpenings()
#dataDAO.loadQuits()
#dataDAO.loadUnemployment()
#dataDAO.loadLocalQuits()

#dataDAO.updateQuitsByID(1, '2010-01-01', 6)

#foo = dataDAO.findQuitsByID(1)
#print(foo)

#dataDAO.insertQuitsByID('2022-12-01', 6)

#dataDAO.deleteQuitsByID(155)

#print(dataDAO.findQuitsByDate('2010-01-01'))

#dataDAO.updateQuitsByDate('2010-01-01', 6)

#dataDAO.deleteQuitsByDate('2022-12-01')

dataDAO.insertUser('Sam', 'Sam', 'stracey@somehwere.com')

#dataDAO.updateUserByID(1, 'ST', 'Foobar1', '1234')

#dataDAO.deleteUserByID(2)

#print(dataDAO.readUnemployment())

#data = dataDAO.readQuits()
# convert to dataframe
#df = pd.DataFrame(data)
#print(df)

#dataDAO.loadLocalQuits()