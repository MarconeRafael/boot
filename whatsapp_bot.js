const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const { exec } = require('child_process');
const app = express();
app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', qr => {
    console.log("Escaneie este QR Code para conectar o bot ao WhatsApp:");
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Bot está pronto!');
});

client.on('message', async msg => {
    console.log(`Mensagem recebida: ${msg.body}`);
    
    try {
        // Garantir que a mensagem está corretamente escapada e enviada
        const safeMessage = msg.body.replace(/(["\\])/g, '\\$1'); // Escape de aspas e barras
        exec(`python caminhoneiro.py "${safeMessage}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Erro ao executar o script Python: ${error.message}`);
                msg.reply("Desculpe, ocorreu um erro ao processar sua mensagem.");
                return;
            }
            if (stderr) {
                console.error(`stderr: ${stderr}`);
                msg.reply("Desculpe, ocorreu um erro ao processar sua mensagem.");
                return;
            }

            const response = stdout.trim();
            console.log("Resposta do script Python:", response);

            if (response) {
                msg.reply(response);
            } else {
                msg.reply("Desculpe, não consegui processar a sua solicitação.");
            }
        });
    } catch (error) {
        console.error("Erro ao comunicar com o backend:", error.message);
        msg.reply("Desculpe, ocorreu um erro ao processar sua mensagem.");
    }
});

client.initialize();

app.listen(3000, () => {
    console.log('Servidor do WhatsApp rodando na porta 3000');
});
