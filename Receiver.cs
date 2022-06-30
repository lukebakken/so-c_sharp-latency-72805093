using System.Diagnostics;

// Created using tutorial for C# receiver from here https://www.rabbitmq.com/tutorials/tutorial-one-dotnet.html
class Receive
{
    public static void Main()
    {
        //ThreadPool.SetMinThreads(200, 200);
        var factory = new ConnectionFactory()
        {
            HostName = "127.0.0.1",
            ConsumerDispatchConcurrency = 200
        };


        int count = 0;
        string queue = "hello";
        var timer = new Stopwatch();

        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            channel.QueueDeclare(queue: queue,
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);

            var consumer = new EventingBasicConsumer(channel);
            consumer.Received += (model, ea) =>
            {
                timer.Stop();
                var body = ea.Body.ToArray();
                //var message = Encoding.UTF8.GetString(body);
                Console.WriteLine($"count: {count++}, TimeBetweenmessages: {timer.Elapsed}, messageSize {body.Length}");
                timer.Restart();
            };
            channel.BasicConsume(queue: queue,
                autoAck: true,
                consumer: consumer);

            timer.Start();

            Console.WriteLine(" Press [enter] to exit.");
            Console.ReadLine();
        }

    }
}