const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('E14 Oracle Service running');
});

app.listen(8080, () => {
  console.log('Server running on port 8080');
});
