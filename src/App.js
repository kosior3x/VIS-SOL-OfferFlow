import React, { useState } from 'react';
import { PDFDownloadLink, Page, Text, View, Document, StyleSheet, Font } from '@react-pdf/renderer';

// REJESTRACJA CZCIONKI (Eliminuje krzaki w PDF)
Font.register({
  family: 'Roboto',
  src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-light-webfont.ttf'
});

const styles = StyleSheet.create({
  page: { padding: 40, fontFamily: 'Roboto', fontSize: 10, position: 'relative' },
  watermark: {
    position: 'absolute', top: '40%', left: '5%', fontSize: 60,
    color: 'rgba(0, 48, 73, 0.05)', transform: 'rotate(-45deg)', fontWeight: 'bold'
  },
  header: { borderBottom: 2, borderColor: '#003049', marginBottom: 20, paddingBottom: 10 },
  table: { display: 'table', width: 'auto', borderStyle: 'solid', borderWidth: 1, borderColor: '#eee' },
  row: { flexDirection: 'row', borderBottomWidth: 1, borderColor: '#eee', minHeight: 25, alignItems: 'center' },
  th: { backgroundColor: '#003049', color: '#fff', fontWeight: 'bold' },
  colLp: { width: '8%', paddingLeft: 5 },
  colDesc: { width: '52%', paddingLeft: 5 },
  colQty: { width: '10%', textAlign: 'center' },
  colNet: { width: '15%', textAlign: 'right', paddingRight: 5 },
  colTotal: { width: '15%', textAlign: 'right', paddingRight: 5 },
});

const OfertaPDF = ({ data }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.watermark}>VIS-SOL OFFICIAL</Text>
      <View style={styles.header}>
        <Text style={{ fontSize: 20, color: '#003049' }}>OFERTA HANDLOWA {data.ohNumber}</Text>
        <Text>Wystawca: Vis-Sol Visuals and Solutions | vis-sol.prv.pl</Text>
      </View>

      <View style={styles.table}>
        <View style={[styles.row, styles.th]}>
          <Text style={styles.colLp}>LP</Text>
          <Text style={styles.colDesc}>Opis</Text>
          <Text style={styles.colQty}>Ilosc</Text>
          <Text style={styles.colNet}>Netto</Text>
          <Text style={styles.colTotal}>Brutto</Text>
        </View>
        {data.items.map((item, i) => (
          <View key={i} style={styles.row}>
            <Text style={styles.colLp}>{i + 1}</Text>
            <Text style={styles.colDesc}>{item.desc}</Text>
            <Text style={styles.colQty}>{item.qty}</Text>
            <Text style={styles.colNet}>{item.finalNet.toFixed(2)}</Text>
            <Text style={styles.colTotal}>{item.rowGross.toFixed(2)}</Text>
          </View>
        ))}
      </View>

      <View style={{ marginTop: 30, textAlign: 'right' }}>
        <Text>Suma Netto: {data.totalNet.toFixed(2)} PLN</Text>
        <Text style={{ fontSize: 18, color: '#d62828', fontWeight: 'bold' }}>DO ZAPŁATY: {data.totalGross.toFixed(2)} PLN</Text>
      </View>
    </Page>
  </Document>
);

export default function App() {
  const [items, setItems] = useState([{ desc: '', qty: 1, cost: 0, margin: 0, vat: 0.23 }]);
  const [discount, setDiscount] = useState(0);

  const calculate = () => {
    let tNet = 0, tGross = 0;
    const processed = items.map(item => {
      const finalNet = item.cost * (1 + item.margin / 100);
      const rowNet = finalNet * item.qty;
      const rowGross = rowNet * (1 + item.vat);
      tNet += rowNet; tGross += rowGross;
      return { ...item, finalNet, rowGross };
    });
    return { items: processed, totalNet: tNet - discount, totalGross: tNet - discount + (tGross - tNet), ohNumber: 'OH/2026/1' };
  };

  return (
    <div style={{ padding: 40, maxWidth: 800, margin: 'auto' }}>
      <h1>VIS-SOL OFFERFLOW PRO</h1>
      {items.map((it, idx) => (
        <div key={idx} style={{ display: 'flex', gap: 10, marginBottom: 10 }}>
          <input placeholder="Opis" onChange={e => {
            const newItems = [...items]; newItems[idx].desc = e.target.value; setItems(newItems);
          }} />
          <input type="number" placeholder="Koszt" onChange={e => {
            const newItems = [...items]; newItems[idx].cost = parseFloat(e.target.value); setItems(newItems);
          }} />
          <input type="number" placeholder="Marża %" onChange={e => {
            const newItems = [...items]; newItems[idx].margin = parseFloat(e.target.value); setItems(newItems);
          }} />
        </div>
      ))}
      <button onClick={() => setItems([...items, { desc: '', qty: 1, cost: 0, margin: 0, vat: 0.23 }])}>+ Dodaj pozycję</button>
      
      <div style={{ marginTop: 20 }}>
        <PDFDownloadLink document={<OfertaPDF data={calculate()} />} fileName="Oferta_VisSol.pdf">
          {({ loading }) => (loading ? 'Przygotowanie...' : 'POBIERZ GOTOWY PDF')}
        </PDFDownloadLink>
      </div>
    </div>
  );
}
