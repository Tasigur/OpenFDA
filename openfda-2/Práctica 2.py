import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
x=repos["results"][0]["active_ingredient"][0]
print(x)
#Aspirin's ability to suppress the production of prostaglandins and thromboxanes is due to its irreversible inactivation of the cyclooxygenase (COX; officially known as prostaglandin-endoperoxide synthase, PTGS) enzyme required for prostaglandin and thromboxane synthesis. Aspirin acts as an acetylating agent where an acetyl group is covalently attached to a serine residue in the active site of the PTGS enzyme (Suicide inhibition). This makes aspirin different from other NSAIDs (such as diclofenac and ibuprofen), which are reversible inhibitors .

#Low-dose aspirin use irreversibly blocks the formation of thromboxane A2 in platelets, producing an inhibitory effect on platelet aggregation during the lifetime of the affected platelet (8–9 days). This antithrombotic property makes aspirin useful for reducing the incidence of heart attacks in people who have had a heart attack, unstable angina, ischemic stroke or transient ischemic attack.[133] 40 mg of aspirin a day is able to inhibit a large proportion of maximum thromboxane A2 release provoked acutely, with the prostaglandin I2 synthesis being little affected; however, higher doses of aspirin are required to attain further inhibition.[134]
search=result.active_ingredient:"ACTIVE INGREDIENT SILICEA HPUS 2X and higher"