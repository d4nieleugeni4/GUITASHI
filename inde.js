const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

// Configuração do cliente
const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: './session' // Pasta onde a sessão será armazenada
    }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Quando o QR code for necessário
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneie o QR code acima para conectar.');
});

// Quando estiver autenticado
client.on('authenticated', () => {
    console.log('Autenticado com sucesso!');
});

// Quando estiver pronto para usar
client.on('ready', () => {
    console.log('Client está pronto!');
});

// Lidando com mensagens
client.on('message', async msg => {
    if (msg.body === '.ping') {
        msg.reply('pong');
    }
});

// Iniciar o cliente
client.initialize();
