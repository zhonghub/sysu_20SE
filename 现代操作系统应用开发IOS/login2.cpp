- (void)login2{
   // NSDictionary *dic = @{@"username":_inputName.text, @"password":_inputPassword.text, @"code":_inputVerify.text, @"uuid":_uuid};
   NSDictionary *dic = @{@"username" : @"admin", @"password" : @"admin123", @"code" : _inputVerify.text, @"uuid" : _uuid};
   NSError *error = nil;
   NSData *jsonData = [NSJSONSerialization dataWithJSONObject:dic options:1 error:&error];
   NSString *jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
   // dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES
   //  urlRequest.HTTPBody = [[NSData alloc] initWithData:[jsonString dataUsingEncoding:NSUTF8StringEncoding]];
   dispatch_semaphore_t sema = dispatch_semaphore_create(0);

   NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString:@"http://172.18.178.57:3000/prod-api/login"]
      cachePolicy:NSURLRequestUseProtocolCachePolicy timeoutInterval:10.0];
   NSDictionary *headers = @{
      @"Content-Type" : @"application/json"
   };

   [request setAllHTTPHeaderFields:headers];
   NSData *postData = [[NSData alloc] initWithData:[jsonString dataUsingEncoding:NSUTF8StringEncoding]];
   [request setHTTPBody:postData];

   [request setHTTPMethod:@"POST"];

   NSURLSession *session = [NSURLSession sharedSession];
   NSURLSessionDataTask *dataTask = [session dataTaskWithRequest:request
      completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
         if (error){
            NSLog(@"%@", error);
            // dispatch_semaphore_signal(sema);
         }
         else{
            // NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
            NSError *parseError = nil;
            // NSDictionary *responseDictionary = [NSJSONSerialization JSONObjectWithData:data options:0 error:&parseError];
            NSDictionary *responseDictionary = [NSJSONSerialization JSONObjectWithData:data options:0 error:&parseError];
            NSLog(@"%@", responseDictionary);
            // dispatch_semaphore_signal(sema);
            NSLog(@"token = %@", responseDictionary[@"token"]);
            NSString *jsonString2 = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
            NSData *jsonData2 = [jsonString2 dataUsingEncoding:NSUTF8StringEncoding];
            NSDictionary *dict = [NSJSONSerialization JSONObjectWithData:jsonData2 options:0 error:nil];
            NSLog(@"response = %@", dict);
            NSLog(@"token = %@", dict[@"token"]);
         }
      }];   
   [dataTask resume];
   // dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER);
}