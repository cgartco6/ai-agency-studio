import React, { useState } from 'react';

function App() {
  const [workspaceId, setWorkspaceId] = useState<number | null>(null);
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [template, setTemplate] = useState('landing.html');
  const [brand, setBrand] = useState({ name: 'ZAR Digital Agency', color: '#7c3aed', tagline: 'AI Execution Engine' });
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(false);
  const [emailStatus, setEmailStatus] = useState('');
  
  const API_BASE = "http://localhost:8000/api/v1";

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: 'secure_password_string', company_name: company })
    });
    const data = await res.json();
    if(data.workspace_id) {
      setWorkspaceId(data.workspace_id);
      alert(`Workspace activated! ID: ${data.workspace_id}`);
    }
  };

  const triggerScraper = async () => {
    if(!workspaceId) return alert("Please register your workspace first.");
    setLoading(true);
    const res = await fetch(`${API_BASE}/scraper/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workspace_id: workspaceId, industry: 'Marketing', location: 'South Africa' })
    });
    const data = await res.json();
    setLeads(data.leads || []);
    setLoading(false);
  };

  const blastOutreachEmails = async () => {
    if (leads.length === 0) return alert("No active target leads found to reach out to.");
    setEmailStatus("Blasting automated cold templates...");
    const res = await fetch(`${API_BASE}/scraper/send-outreach`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workspace_id: workspaceId, target_leads: leads, sender_brand: brand.name })
    });
    const data = await res.json();
    setEmailStatus(`Success: ${data.dispatched_count} outreach emails dispatched!`);
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif', backgroundColor: '#fafafa', minHeight: '100vh', color: '#111' }}>
      <header style={{ borderBottom: '2px solid #eaeaea', paddingBottom: '1.5rem', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800 }}>AI Studio Control Console</h1>
          <p style={{ color: '#666', fontSize: '0.9rem' }}>Enterprise multi-currency stack active</p>
        </div>
      </header>

      {!workspaceId ? (
        <section style={{ maxWidth: '450px', margin: '4rem auto', background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
          <h2 style={{ marginBottom: '1.5rem' }}>Create Studio Workspace</h2>
          <form onSubmit={handleRegister}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Email Address</label>
              <input type="email" required value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
            </div>
            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Agency Name</label>
              <input type="text" required value={company} onChange={e => setCompany(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #ccc' }} />
            </div>
            <button type="submit" style={{ width: '100%', backgroundColor: '#000', color: '#fff', padding: '12px', borderRadius: '6px', fontWeight: 600, border: 'none', cursor: 'pointer' }}>
              Initialize Studio
            </button>
          </form>
        </section>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2.5rem' }}>
          <section style={{ background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
            <h2 style={{ marginBottom: '1.5rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '0.5rem' }}>Dynamic Asset Engine</h2>
            
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Design Layout Variant</label>
              <select value={template} onChange={e => setTemplate(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #ccc', backgroundColor: '#fff' }}>
                <option value="landing.html">Minimalist Tech Landing Page</option>
                <option value="creative.html">Bold Creative Studio Portfolio</option>
                <option value="corporate.html">Sleek Corporate Digital Identity</option>
              </select>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Brand Blueprint Name</label>
              <input type="text" value={brand.name} onChange={e => setBrand({...brand, name: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Tagline Statement</label>
              <input type="text" value={brand.tagline} onChange={e => setBrand({...brand, tagline: e.target.value})} style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ddd' }} />
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Theme Color Hex</label>
              <input type="color" value={brand.color} onChange={e => setBrand({...brand, color: e.target.value})} style={{ width: '100%', height: '45px', border: 'none', cursor: 'pointer' }} />
            </div>

            <form action={`${API_BASE}/generator/build-package`} method="POST" target="_blank">
              <input type="hidden" name="brand_name" value={brand.name} />
              <input type="hidden" name="primary_color" value={brand.color} />
              <input type="hidden" name="tagline" value={brand.tagline} />
              <input type="hidden" name="template_selection" value={template} />
              <button type="submit" style={{ width: '100%', backgroundColor: '#7c3aed', color: '#fff', padding: '12px', borderRadius: '6px', fontWeight: 600, border: 'none', cursor: 'pointer' }}>
                Compile & Export Selection ZIP
              </button>
            </form>
          </section>

          <section style={{ background: '#fff', padding: '2rem', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
            <h2 style={{ marginBottom: '1.5rem', borderBottom: '1px solid #f0f0f0', paddingBottom: '0.5rem' }}>Lead Acquisition & Automated Outreach</h2>
            <button onClick={triggerScraper} disabled={loading} style={{ width: '100%', backgroundColor: '#2563eb', color: '#fff', padding: '12px', borderRadius: '6px', fontWeight: 600, border: 'none', cursor: 'pointer', marginBottom: '1rem' }}>
              {loading ? 'Running Scraper...' : 'Run Lead Generation Pipeline'}
            </button>

            {leads.length > 0 && (
              <button onClick={blastOutreachEmails} style={{ width: '100%', backgroundColor: '#10b981', color: '#fff', padding: '12px', borderRadius: '6px', fontWeight: 600, border: 'none', cursor: 'pointer', marginBottom: '1.5rem' }}>
                💥 Blast Automated Cold Emails
              </button>
            )}

            {emailStatus && <p style={{ color: '#059669', fontSize: '0.9rem', marginBottom: '1rem', fontWeight: 600 }}>{emailStatus}</p>}

            <div style={{ maxHeight: '250px', overflowY: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ textAlign: 'left', borderBottom: '2px solid #f0f0f0' }}>
                    <th style={{ paddingBottom: '0.5rem' }}>Company</th>
                    <th style={{ paddingBottom: '0.5rem' }}>Contact Info</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead: any) => (
                    <tr key={lead.id} style={{ borderBottom: '1px solid #f9f9f9' }}>
                      <td style={{ padding: '0.75rem 0' }}><strong>{lead.company_name}</strong></td>
                      <td style={{ padding: '0.75rem 0' }}><a href={lead.website} style={{ color: '#2563eb', textDecoration: 'none' }}>{lead.email}</a></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;
