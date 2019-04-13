#!/usr/bin/env python
import sys
import re
sys.path.insert(0, '../')  # noqa
from fp import *  # noqa


print('=====  fpu package example =====\n')

# Imperative programming
class EmailValidation:
    emailPtn = re.compile("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")

    def __init__(self):
        pass

    def logError(self, msg):
        print('Error message logged: {}'.format(msg))

    def sendVerificationMail(self, mailAddr):
        print('Mail sent to {}'.format(mailAddr))

    @staticmethod
    def validate(mailAddr):
        if mailAddr is None:
            return Result.failure("Email must not be null")
        elif len(mailAddr) == 0:
            return Result.failure("Email must not be empty")
        elif EmailValidation.emailPtn.match(mailAddr):
            return Result.success()
        else:
            return Result.failure("Email {} is invalid".format(mailAddr))

    def execute(self, mailAddr):
        rst = self.validate(mailAddr)
        if isinstance(rst, Success):
            self.sendVerificationMail(mailAddr)
        else:
            self.logError(rst.message)


emailPtn = re.compile("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")

# FP style implementation
class EmailValidationFP:
    def __init__(self):
        self.succEft = self.sendVerificationMail
        self.failEft = self.logError

    def logError(self, msg):
        print('Error message logged: {}'.format(msg))

    def sendVerificationMail(self, mailAddr):
        print('Mail sent to {}'.format(mailAddr))

    def validate(self, mailAddr):
        return Case.match(Case.default(Result.success(mailAddr)),
                          Case.mcase(Supplier(lambda s: s is None, mailAddr), Result.failure('Email is None')),
                          Case.mcase(Supplier(lambda s: len(s) == 0, mailAddr), Result.failure('Email is empty')),
                          Case.mcase(Supplier(lambda s: not emailPtn.match(s), mailAddr), Result.failure('Email {} is invalid'.format(mailAddr))))

    def execute(self, mailAddr):
        self.validate(mailAddr).bind(self.sendVerificationMail, self.logError)


emailVal1 = EmailValidation()
emailVal2 = EmailValidationFP()

emailVal2.execute("this.is@my.email")
emailVal2.execute(None)
emailVal2.execute("")
emailVal2.execute("john.doe@acme.com")
